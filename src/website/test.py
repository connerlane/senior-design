from helpers import train_model, save_model
from json import load, dump
import numpy as np
m = train_model()

save_model(m)