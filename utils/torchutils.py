import numpy as np
import random
import torch

def initSeeds(seed=1):
	print(f"initSeeds({seed})")
	random.seed(seed)
	torch.manual_seed(seed) 	#turn on this 2 lines when torch is being used
	torch.cuda.manual_seed(seed)
	np.random.seed(seed)


def get_cuda(cudadevice='cuda:0'):
	""" return the best Cuda device """
	devid = cudadevice
	#print ('Current cuda device ', devid, torch.cuda.get_device_name(devid))
	#device = 'cuda:0'	#most of the time torch choose the right CUDA device
	return torch.device(devid)		#use this device object instead of the device string

def onceInit(cudadevice, seed, kCUDA=False):
	#print(f"onceInit {cudadevice}")
	if kCUDA and torch.cuda.is_available():
		if cudadevice is None:
			device = get_cuda()
		else:
			device = torch.device(cudadevice)
			torch.cuda.set_device(device)
	else:
		device = 'cpu'

	print(f"torchutils.onceInit device = {device}")
	torch.backends.cudnn.deterministic = True
	torch.backends.cudnn.enabled = kCUDA

	initSeeds(seed)

	return device

def dumpModelSize(model, details=True):
	total = sum(p.numel() for p in model.parameters())
	if details:
		for name, param in model.named_parameters():
			if param.requires_grad:
				num_params = sum(p.numel() for p in param)
				print(f"name: {name}, num params: {num_params} ({(num_params/total) *100 :.2f}%)")

	print(f"total params: {total}, ", end='')
	print(f"trainable params: {sum(p.numel() for p in model.parameters() if p.requires_grad)}")