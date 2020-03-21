from .util import conv, maxpool, upsample
import numpy as np

class Layer:
    name = 'layer'
    def __init__(self, name):
        self.name = name

    def forward(self, x): pass

    def backward(self, grad_y): pass

    def para(self): return None

    def load(self, buf): return 0

    def __call__(self, x):
        return self.forward(x)

class Dense(Layer):
    name = 'dense'
    def __init__(self, c, n):
        self.K = np.zeros((n, c), dtype=np.float32)
        self.bias = np.zeros(c, dtype=np.float32)

    def para(self): return self.K.shape

    def forward(self, x):
        y = x.dot(self.K.T)
        y += self.bias.reshape((1, -1))
        return y

    def load(self, buf):
        sk, sb = self.K.size, self.bias.size
        self.K.ravel()[:] = buf[:sk]
        self.bias.ravel()[:] = buf[sk:sk+sb]
        return sk + sb

class Conv2d(Layer):
    name = 'conv'
    def __init__(self, c, n, w, s):
        self.n, self.c, self.w, self.s = n, c, w, s
        self.K = np.zeros((n, c, w, w), dtype=np.float32)
        self.bias = np.zeros(n, dtype=np.float32)

    def para(self): return self.n, self.c, self.w, self.s

    def forward(self, x):
        out = conv(x, self.K, (self.s, self.s))
        out += self.bias.reshape((1, -1, 1, 1))
        return out

    def load(self, buf):
        sk, sb = self.K.size, self.bias.size
        self.K.ravel()[:] = buf[:sk]
        self.bias.ravel()[:] = buf[sk:sk+sb]
        return sk + sb

class ReLU(Layer):
    name = 'relu'
    def __init__(self):pass

    def forward(self, x):
        return (x > 0) * x

class Flatten(Layer):
    name = 'flatten'
    def __init__(self):pass

    def forward(self, x):
        return x.reshape((1, -1))

class Sigmoid(Layer):
    name = 'sigmoid'
    def __init__(self):pass

    def forward(self, x):
        return 1/(1 + np.exp(-x))

class Softmax(Layer):
    name = 'softmax'
    def __init__(self, axis=-1):
        self.axis = axis

    def forward(self, x):
        eX = np.exp((x.T - np.max(x, axis=self.axis)).T)
        return (eX.T / eX.sum(axis=self.axis)).T

class Maxpool(Layer):
    name = 'maxpool'
    def __init__(self, stride=2):
        self.stride = stride

    def para(self): return (self.stride,)

    def forward(self, x):
        return maxpool(x, (self.stride, self.stride))

class UpSample(Layer):
    name = 'upsample'
    def __init__(self, k):
        self.k = k

    def para(self): return (self.k,)

    def forward(self, x):
        return upsample(x, self.k)

class Concatenate(Layer):
    name = 'concat'
    def __init__(self): pass

    def forward(self, x):
        return np.concatenate(x, axis=1)

layerkey = {'dense':Dense, 'conv':Conv2d, 'relu':ReLU, 
    'flatten':Flatten, 'sigmoid':Sigmoid, 'softmax': Softmax,
    'maxpool':Maxpool, 'upsample':UpSample, 'concat':Concatenate}

if __name__ == "__main__":
    pass