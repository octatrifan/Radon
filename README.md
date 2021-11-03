# Predicting Indoor Radon Levels Using Machine Learning Algorithms

Research Paper is available [HERE](Paper.pdf).

## Authors

|         Name       |Email Address                        
|----------------|-------------------------------|
|Octavian-Alexandru Trifan|`octatrifan@gmail.com` |           
|Daniel Todașcă          |`todasca7daniel@gmail.com`    |
|Anastasia Susciuc         |`susciuc.anastasia@gmail.com`|

> Computer Science Students 
 Babes-Bolyai University, Cluj-Napoca, Romania
  Research  Institute on  Artificial Intelligence, Virtual Reality and Robotics

## Abstract

Predicting the radon levels represents a pertinent problem in the Machine Learning universe. Although this problem has been approached sparsely in the past, numerous studies recently surfaced in order to find a satisfactory model. In this paper, we are comparing results from three different ML algorithms (Deep Neural Networks, Support Vector Machines and Random Forests) in order to find a satisfactory model.

The aim is to outline the regions where there may exist a risk of high indoor radon concentration, without installing physical sensors to detect those threats. Finding a reliable model has benefits because it significantly reduces the cost associated with the sensors and the time required to gather the physical data.

## Dataset

The dataset used in our experiments is publicaly available [Here](https://beta.geohive.ie/datasets/42d9ccbfacc349f1b1edea8e6369ed7a_1/explore).

> We are expecting dataset offered by researchers from Babes-Bolyai University, Environmental Science and Engineering Faculty, who recorded and measured radon levels periodically in multiple locations. Our future work will be based on this real-life set.
## Contents

### Deep Neural Netorks - [DNN.py](DNN.py)
### Support Vector Machines - [SVM.py](SVM.py)
### Random Forests - [RF.py](RF.py)

>Further explanations about how these algorithms were used are presented in the [paper](Paper.pdf).

## Results

|     Algorithm    |R2   |Acc.training  | Acc. val | MAE testing | MAE Training
|----------------|-------------------------------|-----------------------------| --------- | ----| --|
|DNN|`0.891213` |96.1685% |96.204% | `0.95152` |`0.97703` |
|SVM|`0.95670`  |99.1379%|96.1672% |`0.91407` | `0.3103` |
|RF |`0.90162`|96.7741%| 96.7741% |`1.0822` | `1.0087` |


>This results leads us to believe that in fact, the values we predicted were already predicted by an ML algorithm
 
## Future Work
In collaboration with researchers from Babes-Bolyai University, Environmental Science and Engineering Faculty, we are planning to further develop the algorithms on a real-life dataset, seeking to enhance the public health and safety in Transylvania.
