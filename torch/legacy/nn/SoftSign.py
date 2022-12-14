import torch
from .Module import Module
from .utils import clear

class SoftSign(Module):

    def __init__(self):
        super(SoftSign, self).__init__()
        self.temp = None
        self.tempgrad = None

    def updateOutput(self, input):
        self.temp = self.temp or input.new()
        self.temp.resizeAs_(input).copy_(input).abs_().add_(1)
        self.output.resizeAs_(input).copy_(input).div_(self.temp)
        return self.output

    def updateGradInput(self, input, gradOutput):
        self.tempgrad = self.tempgrad or input.new()
        self.tempgrad.resizeAs_(self.output).copy_(input).abs_().add_(1).mul_(self.tempgrad)
        self.gradInput.resizeAs_(input).copy_(gradOutput).div_(self.tempgrad)
        return self.gradInput

    def clearState(self):
        clear(self, 'temp', 'tempgrad')
        return super(SoftSign, self).clearState()

