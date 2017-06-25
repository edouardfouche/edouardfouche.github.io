---
layout: post
title:  "Fun with Tensorflow - im2txt"
date:   2017-03-22 07:00:00 +0100
comments: true
categories: other
---

I came across the *im2txt* model for *Tensorflow*. It is a model developed by *Google DeepMind* that takes an image as input and creates a caption for it. I used the model to create captions for a few of my own images, and it was a lot of fun ! In this article, I will explain how to play with it. Then, I will show a few examples.  

About the model
---------------

This model won ex-aequo with a team from Microsoft Research an image captioning competition based on the [COCO][COCO] data set. Generating caption for images is an interesting problem, since it leads to a better indexing of images on the web and to the possibility for computers to "understand" images. 

Basically, a deep convolutional neural network is used to encode images to a fixed-length vector representation. It is followed by a long short-term memory (LSTM) network, which takes the encoding and produces a caption. 

I am not going to describe it in detail here. More information can be found in the [github][im2txt] and the [paper][paper] of the model[^fn3]. Now let's move to the fun part ! 

Prerequisites
-------------

We need to clone the `tensorflow/models` folder which contains `im2txt` somewhere in our machine. Personally, I put all my git projects in a `~/git` folder:

```shell
edouard@tower:~/git$ git clone https://github.com/tensorflow/models.git
```
In this small tutorial, I used the version at commit [c226118][c226118]. This is the current version at the writing time of this article, but future versions might work too. 

The following packages are required ([instructions][requirements]): 
- Bazel 
- Tensorflow (version 0.12.1)
- Numpy
- Natural Languages Toolkit (NLTK)

Since we don't want to train the model by ourself (it would take weeks), we download a fine-tuned *checkpoint*, as well as a the corresponding vocabulary file. The checkpoint I found was trained over 3 millions iterations. I recommend to put the `model.ckpt-3000000`, `model.ckpt-3000000.meta` and `word_counts.txt` files in a distinct folder, such as `~/im2txt/`.

- Download the *checkpoint* from [here][finetuned]. 

Run the inference
-----------------

First, we need to build the `run_inference` module with Bazel: 

```shell
edouard@tower:~$ cd ~/git/models/im2txt
edouard@tower:~/git/models/im2txt$ bazel build -c opt im2txt/run_inference
..........
INFO: Found 1 target...
Target //im2txt:run_inference up-to-date:
  bazel-bin/im2txt/run_inference
INFO: Elapsed time: 3.078s, Critical Path: 0.02s
```

Hint: You should make sure that your `$JAVA_HOME` variable is set correctly. I have the following declaration in my `~/.bashrc` file:

```shell
export JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
```

Then, you should be good to go ! I placed the image I wanted to caption (`img.jpg`) in the `~/im2txt/` folder and did the following: 

```shell
edouard@tower:~$ CHECKPOINT_DIR="${HOME}/im2txt/model.ckpt-3000000"
edouard@tower:~$ IMAGE_FILE="${HOME}/im2txt/img.jpg"
edouard@tower:~$ VOCAB_FILE="${HOME}/im2txt/word_counts.txt"

edouard@tower:~$ cd ~/git/models/im2txt

edouard@tower:~/git/models/im2txt$ bazel-bin/im2txt/run_inference \
  				   --checkpoint_path=${CHECKPOINT_DIR} \
                                   --vocab_file=${VOCAB_FILE} \
                                   --input_files=${IMAGE_FILE}
```

This will probably not work on the first run. Depending on your Tensorflow/Python version, you might need to hack around a bit. For your information, I use Tensorflow 0.12.1 and Python 3.5.2. The modifications are mostly due to changes in the Tensorflow API and to Python2/3 differences.

I would recommend you to try the following changes only if Python complains: 

- In `~/git/im2txt/im2txt/show_and_tell_model.py`:

At line 247:
```python
lstm_cell = tf.contrib.rnn.BasicLSTMCell( #to:
```
```python
lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(
```

At line 267:
```python
tf.concat(axis=1, values=initial_state, name="initial_state") #to:
```
```python
tf.concat(concat_dim=1, values=initial_state, name="initial_state")
```

At line 273:
```python
state_tuple = tf.split(value=state_feed, num_or_size_splits=2, axis=1) #to:
```
```python
state_tuple = tf.split(value=state_feed, num_split=2, split_dim=1)
```

At line 281:
```python
tf.concat(axis=1, values=state_tuple, name="state") #to:
```
```python
tf.concat(concat_dim=1, values=state_tuple, name="state")
```

- In `~/git/im2txt/im2txt/inference_utils/vocabulary.py`:

At line 49: 

```python
reverse_vocab = [line.split()[0] for line in reverse_vocab] # to:
```
```python
reverse_vocab = [eval(line.split()[0]).decode() for line in reverse_vocab]
```

The following pages helped me finding the required modifications:
- [rnn_cell has no BasicLSTMCell #6432][Discussion2]
- [Pretrained model for img2txt? #466][Discussion1]


When everything works, you get the top 3 results of what the network thinks your image represents, printed in the shell.

CPU Only:
```shell
INFO:tensorflow:Building model.
INFO:tensorflow:Initializing vocabulary from file: /home/edouard/im2txt/word_counts.txt
INFO:tensorflow:Created vocabulary with 11520 words
INFO:tensorflow:Running caption generation on 1 files matching /home/edouard/im2txt/img.jpg
INFO:tensorflow:Loading model from checkpoint: /home/edouard/im2txt/model.ckpt-3000000
INFO:tensorflow:Successfully loaded checkpoint: model.ckpt-3000000
Captions for image img.jpg:
  0) a man sitting on top of a wooden bench next to a tree . <S> <S> . <S> (p=0.000005)
  1) a man sitting on top of a wooden bench next to a forest . <S> <S> . <S> (p=0.000004)
  2) a man sitting on top of a wooden bench next to a tree . <S> <S> <S> . (p=0.000004)
edouard@tower:~/git/models/im2txt$ 
```

With GPU:
```shell
I tensorflow/stream_executor/dso_loader.cc:128] successfully opened CUDA library libcublas.so locally
I tensorflow/stream_executor/dso_loader.cc:128] successfully opened CUDA library libcudnn.so locally
I tensorflow/stream_executor/dso_loader.cc:128] successfully opened CUDA library libcufft.so locally
I tensorflow/stream_executor/dso_loader.cc:128] successfully opened CUDA library libcuda.so.1 locally
I tensorflow/stream_executor/dso_loader.cc:128] successfully opened CUDA library libcurand.so locally
I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:937] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
I tensorflow/core/common_runtime/gpu/gpu_device.cc:885] Found device 0 with properties: 
name: GeForce GTX 970
major: 5 minor: 2 memoryClockRate (GHz) 1.253
pciBusID 0000:01:00.0
Total memory: 3.94GiB
Free memory: 3.45GiB
I tensorflow/core/common_runtime/gpu/gpu_device.cc:906] DMA: 0 
I tensorflow/core/common_runtime/gpu/gpu_device.cc:916] 0:   Y 
I tensorflow/core/common_runtime/gpu/gpu_device.cc:975] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GeForce GTX 970, pci bus id: 0000:01:00.0)
Captions for image img.jpg:
  0) a man sitting on top of a wooden bench next to a tree . <S> <S> . <S> (p=0.000005)
  1) a man sitting on top of a wooden bench next to a forest . <S> <S> . <S> (p=0.000004)
  2) a man sitting on top of a wooden bench next to a tree . <S> <S> <S> . (p=0.000004)
edouard@tower:~/git/models/im2txt$ 
```

Creating  a caption for an image using the GPU takes about 8 seconds. Most of the time is spent loading the CUDA library, so it would be more efficient to create captions for a bunch of images in a row. This is possible, if you separate the paths to the files with a comma. With CPU only, it took about 12 seconds. As long as you don't plan to train the model yourself, a modern CPU is just fine. 

Results
-------

I let the inference run on a bunch of pictures I took in the past. Sometimes, I've got very unexpected results and it was really funny ! When pictures are a bit abstract, or contain unusual objects, it fails. Here I would like to share a few of my good and no-so-good results. 

<br>

{:.center}
![img](/img/fun-with-tensorflow-im2txt/img.jpg){:class="img-responsive"}
{:style="max-width: 500px; margin: auto"}
**A man sitting on top of a wooden bench next to a tree.**
{:style="text-align: center"}

This one is very accurate. Just the formulation "on top of a wooden bench" sounds a bit robotic to me.

<br><br>

![img2](/img/fun-with-tensorflow-im2txt/img2.jpg){:class="img-responsive"}

**A group of people sitting around a table eating food**
{:style="text-align: center"}

This one is also great ! By the way, those two guys are my friends [Daniel][Daniel] and [Maxim][Maxim]. They are awesome ! 

<br><br>

![img18](/img/fun-with-tensorflow-im2txt/img18.jpg){:class="img-responsive"}

**A bike is parked next to a fence.**
{:style="text-align: center"}

Very good too. Maybe it could have said something about the river and the trees. 

<br><br>

![img20](/img/fun-with-tensorflow-im2txt/img20.jpg){:class="img-responsive"}

**A couple of birds that are standing in some water.** 
{:style="text-align: center"}

Correct ! Though the water is in the background. 

<br><br>

![img27](/img/fun-with-tensorflow-im2txt/img27.jpg){:class="img-responsive"}

**A close up of a television set with a keyboard.**
{:style="text-align: center"}

Actually, the object in the picture is a device used to analyze numerical circuits. The model certainly does not know what it is, but the approximation to a television makes a lot of sense. Also, the different keys together certainty look a bit like a keyboard. 

<br><br>

![img11](/img/fun-with-tensorflow-im2txt/img11.jpg){:class="img-responsive"}

**A group of people standing on top of a sandy beach.**
{:style="text-align: center"}

This one is partly wrong. Obviously, it did not get the [*tilt-shift*][tilt-shift] effect that makes the scenery look miniaturized. However, because of the black & white grain I understand why it thinks there is sand. 

<br><br>

![img9](/img/fun-with-tensorflow-im2txt/img9.jpg){:class="img-responsive"}

**A close up of a small bird on a table.**
{:style="text-align: center"}

This is not so good. Clearly, it is an animal (actually, an [axolotl][axolotl]) but it is quite different from a bird. Also, I can't see the table ! 

<br><br>

![img30](/img/fun-with-tensorflow-im2txt/img30.jpg){:class="img-responsive"}

**A group of people standing next to a train in the background.**
{:style="text-align: center"}

There are indeed people in the background (monks praying, but they are really out of focus). I think it falsely interpreted the candles as people. The idea of a train makes some sense, because the iron candle rails remind a bit of train tracks.

<br><br>  

![img15](/img/fun-with-tensorflow-im2txt/img15.jpg){:class="img-responsive"}

**A small bird sitting on top of a wooden bench.**
{:style="text-align: center"}

Oops ! It did not get the picture at all, probably because it is too abstract. 

<br><br>

<br><br>

![img31](/img/fun-with-tensorflow-im2txt/img31.jpg){:class="img-responsive"}

**A close up of a person holding a pair of scissors.**
{:style="text-align: center"}

Maybe that's the worst result I've got. That is probably because the model did not learn butterflies ! 

<br>

Conclusion
----------

To conclude, I would say that the model performs quite well on a restricted range of examples. As long as the picture contains only common objects, it is able to produce meaningful captions. If the picture requires a certain level of abstraction, results are unpredictable. 

This observation is not surprising, because the network was trained only with images containing simple objects at a relatively low level of abstraction: The model can only get at most as good as the data. At the following [link][COCO/explore], you can see the different objects of the COCO data set and query examples of images. 

How could we do better? One solution would be to improve the training set. This might work, but would be very costly: Currently, the COCO data set contains several hundred thousands of images to represent 80 objects only. The number of images we would need to segment and annotate to represent the vast variety of the existing objects is intractable. 

Also, it is unclear yet how to train neural networks to understand abstract concepts. Certainly, progress in other - but connected - areas are required. I believe that a fundamental shift should happen in the focus of the task: from *recognizing* to *interpreting*. 

The key would be to make neural networks learn from fewer examples and to let them learn in an unsupervised way (we are speaking about the so-called *one-shot*[^fn1] and *zero-shot*[^fn2] learning problems). That is to say, they should learn without us telling them all over again the correct labels. For example, as humans, we don't need to see several thousands of examples of cars to recognize cars. 

Obviously, this is an open research problem. 

I wanted to use the model to create captions for my own photographs. For example, I would like to have a bot that could go to my [Flickr][flickr] or my [Facebook][facebook] and add automatically good captions to all the images I post. I must say it is rather unlikely for me to use the model to do that, because it may create a lot of meaningless tags. I would probably wait for better results !  

Try it yourself !
-----------------

Using the instructions, I guess you should be able to run the model yourself with little work ! Don't hesitate to share your results ! :)   

Sources
-------

[^fn1]: Fei-Fei L., Fergus R., & Perona P. (2006). *One-shot learning of object categories*. IEEE Transactions on Pattern Analysis and Machine Intelligence.

[^fn2]: Palatucci M., Hinton G. E., Pomerleau D. & Mitchell, T. M. (2009). *Zero-Shot Learning with Semantic Output Codes*. Neural Information Processing Systems.

[^fn3]: Vinyals O., Toshev A., Bengio S. & Erhan D. (2016). *Show and Tell: Lessons learned from the 2015 MSCOCO Image Captioning Challenge*. IEEE Transactions on Pattern Analysis and Machine Intelligence.

[COCO]:http://mscoco.org/
[paper]: https://arxiv.org/abs/1609.06647
[im2txt]: https://github.com/tensorflow/models/tree/master/im2txt
[flickr]: https://www.flickr.com/photos/edouardf
[facebook]: https://www.facebook.com/edouardf
[finetuned]: https://drive.google.com/file/d/0B_qCJ40uBfjEWVItOTdyNUFOMzg/view
[Daniel]: http://www.danielrojas.net/
[Maxim]: http://www.maximlapis.com/
[c226118]: https://github.com/tensorflow/models/tree/c22611891d0826bbf656a367874489c0dad95777

[Discussion1]: https://github.com/tensorflow/models/issues/466#issuecomment-254002590
[Discussion2]: https://github.com/tensorflow/tensorflow/issues/6432

[COCO/explore]: http://mscoco.org/explore/

[requirements]:https://github.com/tensorflow/models/tree/master/im2txt#install-required-packages

[tilt-shift]: https://en.wikipedia.org/wiki/Tilt%E2%80%93shift_photography

[axolotl]:https://en.wikipedia.org/wiki/Axolotl