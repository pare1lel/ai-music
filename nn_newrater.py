import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import pickle

import numpy as np
from sub_rater import rater

MELODY_LENGTH = 64
input_size = 17
hidden_size = 8
num_epochs = 1000

class net(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)  
        self.fc2 = nn.Linear(hidden_size, 1)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = torch.sigmoid(x)
        return x

if __name__ == '__main__':
    train_data = pd.read_csv('./output-all.csv')
    train_size = train_data.shape[0] #训练集大小
    print("train size =", train_size)
    
    for i in range(train_size):
        train_data['Record'][i] = eval(train_data['Record'][i]) # warning, but OK
        print(len(train_data['Record'][i]))
    
    print(train_data)
    
    songs = train_data['Record']
    rating = train_data['Score']
            
    model = net(input_size, hidden_size)
    
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005)  # Adam优化器
    
    train_target = []
    cur_train_input = []
    
    for i in range(train_size):
        cur_train_input.append(rater(songs[i]))
        train_target.append(rating[i])
    
    train_input = torch.tensor(cur_train_input)
    train_target = torch.tensor([train_target], dtype = torch.float32).T
    
    for epoch in range(num_epochs):
        outputs = model(train_input)
        loss = criterion(outputs, train_target)
    
        # 反向传播和优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
    
    pickle.dump(model, open("model.dat", "wb"))