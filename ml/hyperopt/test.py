from hyperopt import hp, fmin, tpe, STATUS_OK, Trials


# 一个函数fmin：fmin(fn, space, algo, max_evals, trials=None)
# fmin寻找最佳匹配的的space，使得fn(目标函数)的返回值最小，采用tpe/random/anneal搜索算法，反复尝试n次，最终得到最佳参数值
# algo指定搜索算法，目前支持以下算法(引用方式：from hyperopt import anneal, tpe, rand)：
# 1.随机搜索(hyperopt.rand.suggest)
# 2.模拟退火(hype ropt.anneal.suggest)
# 3.TPE算法（hyperopt.tpe.suggest，算法全称为Tree-structured Parzen Estimator Approach)

# space
# hp.choice(label, options)  label表示参数名称，options可以是元组或列表。 如果需要枚举从[1, 100]，那么用choice，而不应该用quniform
# hp.randint(label, upper) 返回 [0, upper) 范围内的随机整数，一般用作随机数的种子值。如果这个值会影响loss函数，那么需要考虑使用quniform
# hp.uniform(label, low, high) 返回low和high之间的一个均匀分布数字
# hp.quniform(label, low, high, q) 返回 round(uniform(low,high)/q)*q，适用于那些离散的取值 简单的理解为取 [low, high] 中能被q整除的整数
# hp.pchoice(label, options)  根据概率返回相应值  options: [(probability, value), (probability, value)]
# hp.normal(label, mu, sigma)  返回一个正态分布的实值，均值为mu和标准差为sigma。优化时，这是一个无约束变量

# Trails:用来记录每次eval时，具体使用了什么参数以及相关的返回值。这时候，fn的返回值变为dict，除了loss，还有一个status。Trials对象将数据存储为一个BSON对象，可以利用MongoDB做分布式运算。

space = {
    'x': hp.uniform('x', -5, 5)
}


# 目标函数
def fn(params):
    x = params['x']
    val = x ** 2
    return {'loss': val, 'status': STATUS_OK}


if __name__ == '__main__':
    trials = Trials()
    best = fmin(fn, space=space, algo=tpe.suggest, max_evals=10, trials=trials)
    print('best:', best)
    print('trails:')
    for trial in trials.trials:
        print(trial)