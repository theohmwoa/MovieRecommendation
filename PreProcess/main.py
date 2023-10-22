import pandas as pd
from surprise import Dataset, Reader
from surprise.model_selection import cross_validate
from surprise import SVD
import pickle
import time
import os
from tqdm import tqdm
import itertools


def load_ratings():
    ratings = pd.read_csv('../data/ratings.csv')
    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
    return data


def train_best_model(data, param_grid):
    combinations = list(itertools.product(param_grid['n_epochs'],
                                          param_grid['lr_all'],
                                          param_grid['reg_all']))

    best_rmse = float('inf')
    best_params = None

    for comb in tqdm(combinations, total=len(combinations)):
        model = SVD(n_epochs=comb[0], lr_all=comb[1], reg_all=comb[2])
        results = cross_validate(model, data, measures=['rmse', 'mae'], cv=5)
        mean_rmse = sum(results['test_rmse']) / len(results['test_rmse'])

        if mean_rmse < best_rmse:
            best_rmse = mean_rmse
            best_params = {'n_epochs': comb[0], 'lr_all': comb[1], 'reg_all': comb[2]}

    print(f"Best RMSE score: {best_rmse:.4f}")
    print(f"Best parameters: {best_params}")

    best_model = SVD(**best_params)
    trainset = data.build_full_trainset()
    best_model.fit(trainset)

    current_time = time.strftime("%Y%m%d-%H%M%S")
    model_filename = f'models/best_svd_model-{current_time}.pkl'

    if not os.path.exists('../models'):
        os.makedirs('../models')

    with open(model_filename, 'wb') as model_file:
        pickle.dump(best_model, model_file)

    print(f"Model saved to {model_filename}")


param_grid = {
    'n_epochs': [15], #THOSE VALUES SHOULD BE CHANGED I REMOVED THE ONES THAT WORKED FOR ME
    'lr_all': [0.011], #THOSE VALUES SHOULD BE CHANGED I REMOVED THE ONES THAT WORKED FOR ME
    'reg_all': [0.1] #THOSE VALUES SHOULD BE CHANGED I REMOVED THE ONES THAT WORKED FOR ME
}

data = load_ratings()
train_best_model(data, param_grid)
