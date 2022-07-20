from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from hyperopt import hp, fmin, tpe, STATUS_OK, Trials
import matplotlib.pyplot as plt
iris = datasets.load_iris()
x = iris.data
y = iris.target


def hyperopt_train_test(params):
    clf = KNeighborsClassifier(**params)
    return cross_val_score(clf, x, y).mean()


space4knn = {
    'n_neighbors': hp.choice('n_neighbors', range(1, 60))
}


def f(params):
    acc = hyperopt_train_test(params)
    return {'loss': -acc, 'status': STATUS_OK}


if __name__ == '__main__':
    trials = Trials()
    best = fmin(f, space4knn, algo=tpe.suggest, max_evals=100, trials=trials)
    print('best:', best)

    f, ax = plt.subplots(1)
    xs = [t['misc']['vals']['n_neighbors'] for t in trials.trials]
    ys = [-t['result']['loss'] for t in trials.trials]
    ax.scatter(xs, ys, s=20, linewidth=0.01, alpha=0.5)
    ax.set_title('Iris Dataset - KNN', fontsize=18)
    ax.set_xlabel('n_neighbors', fontsize=12)
    ax.set_ylabel('cross validation accuracy', fontsize=12)
    plt.show()
