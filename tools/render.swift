// Render pages in WebKit (WKWebView, the engine of Safari) for before/after checks. macOS only.
//
// Build:  swiftc -O -swift-version 5 -o /tmp/render tools/render.swift
// Run:    /tmp/render <base URL> <output dir> <path>...
//         e.g. /tmp/render http://127.0.0.1:4000 /tmp/shots-after / /about/ /Hello-World/
// Env:    WIDTHS=1280,375   window widths (default 1280,375)
//         AXE=/path/axe.min.js   also run axe-core (WCAG 2.0-2.2 A/AA + best practices) on each page
//
// For each page and width it writes a full-page screenshot <name>-<width>.png (1x, capped at 16000 px),
// and at 375 px it taps the phone menu button and writes <name>-375-menu.png. results.json lists, per
// page and width: navbar height, overflow (elements wider than the window), Caladea font states,
// MathJax formula count, phone menu state and (with AXE) the axe violations.
// Simple Analytics, giscus and Google Forms are blocked (no page views, deterministic screenshots).
// Compare two runs with tools/compare_shots.py. Hidden WebKit windows are throttled: a full run of
// 27 pages x 2 widths can take 10-20 minutes.
import Cocoa
import WebKit

let args = CommandLine.arguments
guard args.count >= 4 else {
    print("usage: render <base URL> <output dir> <path>...")
    exit(2)
}
let base = args[1]
let outDir = args[2]
let paths = Array(args.dropFirst(3))
let env = ProcessInfo.processInfo.environment
let widths: [CGFloat] = (env["WIDTHS"] ?? "1280,375").split(separator: ",").compactMap { Double($0) }.map { CGFloat($0) }
let axeSource: String? = env["AXE"].flatMap { try? String(contentsOfFile: $0, encoding: .utf8) }

let mathStateJS = """
const tag = document.querySelector('script[src*="MathJax.js"]');
if (!tag) return 'no-script';
if (typeof MathJax === 'undefined' || !MathJax.Hub || !MathJax.isReady) return 'loading';
const q = MathJax.Hub.queue;
return (q.pending === 0 && !q.running) ? 'idle' : 'busy';
"""

let factsJS = """
const vw = document.documentElement.clientWidth;
const wide = [];
for (const el of document.body.querySelectorAll('*')) {
  const r = el.getBoundingClientRect();
  if (r.width > 0 && r.right > vw + 1) wide.push(el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + ' right=' + Math.round(r.right));
}
const nav = document.querySelector('.navbar');
return JSON.stringify({
  title: document.title,
  height: document.documentElement.scrollHeight,
  overflow: document.documentElement.scrollWidth > vw,
  wide: wide.slice(0, 6),
  navbarHeight: nav ? Math.round(nav.getBoundingClientRect().height) : null,
  formulas: document.querySelectorAll('span.MathJax').length,
  fonts: [...document.fonts].filter(f => f.family.includes('Caladea')).map(f => f.weight + (f.style === 'italic' ? 'i' : '') + ':' + f.status).join(' ')
});
"""

let axeJS = """
const r = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice'] }, resultTypes: ['violations'] });
return JSON.stringify(r.violations.map(v => ({ id: v.id, impact: v.impact, count: v.nodes.length, targets: v.nodes.slice(0, 3).map(n => n.target.join(' ')) })));
"""

let menuJS = """
const t = document.querySelector('.navbar-toggle');
if (!t) return 'no-toggle';
t.click();
await new Promise(r => setTimeout(r, 700));
const c = document.querySelector('.navbar-collapse');
return c && c.classList.contains('in') ? 'opens' : 'does-not-open';
"""

@MainActor
final class Runner: NSObject, WKNavigationDelegate {
    let window: NSWindow
    let webView: WKWebView
    var cont: CheckedContinuation<Void, Never>?
    var results: [[String: Any]] = []

    override init() {
        window = NSWindow(contentRect: NSRect(x: -20000, y: -20000, width: 1280, height: 900),
                          styleMask: [.borderless], backing: .buffered, defer: false)
        webView = WKWebView(frame: NSRect(x: 0, y: 0, width: 1280, height: 900), configuration: WKWebViewConfiguration())
        super.init()
        webView.navigationDelegate = self
        window.contentView = webView
        window.orderBack(nil)
    }

    func block() async {
        let rules = """
        [{"trigger":{"url-filter":"simpleanalyticscdn\\\\.com"},"action":{"type":"block"}},
         {"trigger":{"url-filter":"giscus\\\\.app"},"action":{"type":"block"}},
         {"trigger":{"url-filter":"docs\\\\.google\\\\.com"},"action":{"type":"block"}}]
        """
        if let list = try? await WKContentRuleListStore.default().compileContentRuleList(forIdentifier: "render", encodedContentRuleList: rules) {
            webView.configuration.userContentController.add(list)
        }
    }

    nonisolated func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) { Task { @MainActor in self.finish() } }
    nonisolated func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) { Task { @MainActor in self.finish() } }
    nonisolated func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!, withError error: Error) { Task { @MainActor in self.finish() } }
    func finish() { cont?.resume(); cont = nil }

    func setSize(_ w: CGFloat, _ h: CGFloat) {
        window.setContentSize(NSSize(width: w, height: h))
        webView.frame = NSRect(x: 0, y: 0, width: w, height: h)
    }
    func pause(_ s: Double) async { try? await Task.sleep(nanoseconds: UInt64(s * 1e9)) }
    func js(_ code: String) async -> String? {
        (try? await webView.callAsyncJavaScript(code, arguments: [:], in: nil, contentWorld: .page)) as? String
    }

    func snapshot(_ w: CGFloat, _ h: CGFloat, _ file: String) async -> Bool {
        let sc = WKSnapshotConfiguration()
        sc.rect = CGRect(x: 0, y: 0, width: w, height: h)
        sc.snapshotWidth = NSNumber(value: Double(w / max(window.backingScaleFactor, 1)))
        guard let img = try? await webView.takeSnapshot(configuration: sc),
              let tiff = img.tiffRepresentation, let rep = NSBitmapImageRep(data: tiff),
              let png = rep.representation(using: .png, properties: [:]) else { return false }
        return (try? png.write(to: URL(fileURLWithPath: file))) != nil
    }

    func run() async {
        try? FileManager.default.createDirectory(atPath: outDir, withIntermediateDirectories: true)
        await block()
        for path in paths {
            let name = (path == "/" ? "home" : path.trimmingCharacters(in: CharacterSet(charactersIn: "/")).replacingOccurrences(of: "/", with: "_"))
            for w in widths {
                setSize(w, 900)
                await withCheckedContinuation { c in
                    cont = c
                    webView.load(URLRequest(url: URL(string: base + path)!))
                    Task { @MainActor in try? await Task.sleep(nanoseconds: 30_000_000_000); self.finish() }
                }
                await pause(1.5)
                for _ in 0..<50 {  // wait for MathJax, at most 25 s
                    let state = await js(mathStateJS) ?? "?"
                    if state == "no-script" || state == "idle" { break }
                    await pause(0.5)
                }
                var row: [String: Any] = ["path": path, "width": Int(w)]
                row["facts"] = await js(factsJS) ?? "{}"
                if let axe = axeSource {
                    _ = try? await webView.evaluateJavaScript(axe)
                    row["axe"] = await js(axeJS) ?? "[]"
                }
                let h = (try? await webView.evaluateJavaScript("document.documentElement.scrollHeight") as? Double) ?? 900
                let fullH = CGFloat(min(h, 16000))
                setSize(w, fullH)
                await pause(3.0)  // lazy images and progressive JPEGs
                let shot = "\(outDir)/\(name)-\(Int(w)).png"
                if await snapshot(w, fullH, shot) { row["shot"] = shot }
                if w == 375 {
                    row["menu"] = await js(menuJS) ?? "error"
                    setSize(w, 700)
                    await pause(0.8)
                    _ = await snapshot(w, 700, "\(outDir)/\(name)-375-menu.png")
                }
                results.append(row)
                FileHandle.standardError.write("done \(path) @\(Int(w))\n".data(using: .utf8)!)
            }
        }
        let data = try! JSONSerialization.data(withJSONObject: results, options: [.prettyPrinted])
        try! data.write(to: URL(fileURLWithPath: "\(outDir)/results.json"))
    }
}

let app = NSApplication.shared
app.setActivationPolicy(.prohibited)
Task { @MainActor in
    await Runner().run()
    exit(0)
}
app.run()
