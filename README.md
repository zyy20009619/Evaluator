# Evaluator工具介绍

## 功能

- **单版本度量功能：根据项目功能依赖文件度量项目质量**

     ```python
     python measure.py -opt sv -obj [object] -pro [project_path] -ver [version] <-dep [dep_path]> -out [out_path]
     ```

+ **多版本度量功能：根据多版本依赖结果度量每个项目质量，并给出项目生长曲线图**

  ```python
  python measure.py -opt mv -obj [object] -pro [project_path] -ver [version] <-dep [dep_path]> -out [out_path]
  ```

+ **对度量结果进行对比：根据两个版本度量结果对比，给出模块质量腐化热点图(diff_result.xlsx)**

  ```
  python measure.py -opt com -c1 [old_path] -c2 [new_path] -out [out_path]
  ```

- **定位可维护性问题根因：根据模块腐化情况，定位导致腐化的根因**

  ```
  python measure.py -opt det -diff [diff_path] -out [out_path]
  ```

## 命令说明

 ```python
 usage: measure.py [-h] [-opt OPT] [-obj OBJ] [-ver VER] [-pro PRO] [-dep DEP] [-c1 C1] [-c2 C2] [-diff DIFF] [-out OUT]
     
   -h, --help  show this help message and exit
   -opt OPT    必选参数，功能选项，提供sv/mv/com/det四种选择
   -obj OBJ    处理对象，目前提供aosp/honor/others三种场景(除com功能，其他功能下此选项为必选参数)
   -ver VER    处理版本，若为单版本度量不存在版本号请输入main作为版本号，若为多版本使用?连接不同版本号
   -pro PRO    项目路径(除com/det功能，其他功能下此选项为必选参数)
   -dep DEP    可选参数，依赖文件路径，若输入应遵循示例所示格式，若不输入工具会自动生成依赖文件到out_path
   -c1 C1      对比功能较老版本度量结果路径，路径下需包含measure_result.json和dep.json
   -c2 C2      对比功能较新版本度量结果路径，路径下需包含measure_result.json和dep.json
   -diff DIFF  定位功能输入路径，路径包含measure_diff.json和dep_diff.json
   -out OUT    必选参数，结果输出文件夹
 ```

##### **dep_path示例如下：**

![image-20220720113705869](./image/dep_path.png)

## 使用方法

1. 直接使用

   使用`python measure.py -opt...`使用

2. 打包为可执行文件使用

   ```
   pip install Pyinstaller
   Pyinstaller -F measure.py -p 项目路径
   ```

   打包完成后在dist目录下执行`measure.exe -opt ...`使用（注意：不要挪动dist下jar包位置）

## 指标说明

本度量工具共提供4个粒度的项目可维护性度量，每个粒度提供的指标数量统计如下：

| 粒度    | 指标数量 |
| ------- | -------- |
| project | 11       |
| module  | 12       |
| class   | 42       |
| method  | 12       |
- ### project

| 指标                              | 来源 | 说明                                                         |
| --------------------------------- | ---- | ------------------------------------------------------------ |
| score                             | [1]  | 对模块级指标进行融合得到模块可维护性的综合评分               |
| CHM                               | [2]  | 项目中所有模块在消息层内聚程度的均值。                       |
| CHD                               | [2]  | 项目中所有模块在领域层内聚程度的均值。                       |
| SMQ(structural modularity)        | [2]  | 结构模块化程度。SMQ 值越大,说明模块的模块化程度越高。        |
| SPREAD                            | [3]  | 度量模块中的实体在演化过程中横切协同变化集群的个数。SPREAD越小，总体模块性越好。 |
| FOCUS                             | [3]  | 度量模块化良好的程度。FOCUS越大，总体模块性越好。            |
| ICF(intra co-change frequency)    | [2]  | 所有模块演化内部共变频率的平均值。ICF越高，总体模块内的实体更有可能一起演化。 |
| ECF(external co-change frequency) | [2]  | 所有模块演化外部共变频率的平均值。ECF越低，总体跨模块边界的实体更有可能独立演化。 |
| REI(ratio of ecf to icf)          | [2]  | 所有模块演化外部共变频率与内部共变频率的比值的平均值。REI越低，说明总体不同模块一起修改的可能性越低，各模块更有可能会独立演化、独立维护。 |
| ODD(out-degree dependence)        | [2]  | ODD越大，总体耦合其他模块的程度越高，模块之间的动态交互度越高。 |
| IDD(in-degree dependence)         | [2]  | IDD越大，总体被耦合的程度越高，模块间的动态交互程度越高。    |

- ### module

| 指标   | 来源 | 说明                                                         |
| ------ | ---- | ------------------------------------------------------------ |
| scoh   | [2]  | scoh越大，模块内的结构内聚程度越大。                         |
| scop   | [2]  | scop越大，模块间的结构耦合程度越大。                         |
| odd    | [2]  | odd越大，该模块耦合其他模块的程度越高，模块之间的动态交互度越高。 |
| idd    | [2]  | idd越大，该模块被耦合的程度越高，模块间的动态交互程度越高。  |
| spread | [3]  | 度量模块中的实体在演化过程中接触的共变集群个数。spread越小，模块性越好。 |
| focus  | [3]  | 度量模块中的实体在演化过程中专注自身演进的程度。focus越大，模块性越好。 |
| icf    | [2]  | icf越高，模块内的实体更有可能一起演化。                      |
| ecf    | [2]  | ecf越低，跨模块边界的实体更有可能独立演化。                  |
| rei    | [2]  | rei越低，说明不同模块一起修改的可能性越低，模块更有可能会独立演化、独立维护。 |
| DSM    | [4]  | DSM越大，模块越复杂，与外部耦合的可能性越高。                |
| chm    | [2]  | chm越大，模块在消息层内聚程度越高。                          |
| chd    | [2]  | chd越大，模块在领域层内聚程度越高。                          |

- ### class

| 指标                   | 来源 | 说明                                        |
| ---------------------- | ---- | ------------------------------------------- |
| CIS                    | [4]  | 类中公共接口数                              |
| NOM                    | [4]  | 类中方法总数                                |
| NOP                    | [4]  | 多态方法数量                                |
| NAC                    | [4]  | 类继承树深度                                |
| NDC                    | [4]  | 派生类个数                                  |
| NOI                    | ours | 类导入依赖的个数                            |
| NOID                   | ours | 类被导入依赖的个数                          |
| CTM                    | [5]  | 调用方法个数(除自身类中方法)                |
| IDCC                   | [4]  | 模块内耦合类数量                            |
| IODD                   | ours | 模块内耦合其他类的数量                      |
| IIDD                   | ours | 模块内被其他类耦合的数量                    |
| EDCC                   | [4]  | 模块外耦合类数量                            |
| c_FAN_IN               | [5]  | 类扇入                                      |
| c_FAN_OUT              | [5]  | 类扇出                                      |
| CBC                    | [5]  | 类依赖的数量(包含被依赖)                    |
| c_chm                  | [2]  | 类在消息层的功能内聚度                      |
| c_chd                  | [2]  | 类在领域层的功能内聚度                      |
| c_variablesQty         | [5]  | 类中变量数量                                |
| privateMethodsQty      | [5]  | 私有方法数量                                |
| protectedMethodsQty    | [5]  | 保护方法数量                                |
| staticMethodsQty       | [5]  | 静态方法数量                                |
| defaultMethodsQty      | [5]  | 缺省方法数量                                |
| abstractMethodsQty     | [5]  | 抽象方法数量                                |
| finalMethodsQty        | [5]  | final方法数量                               |
| synchronizedMethodsQty | [5]  | synchronized方法数量                        |
| publicFieldsQty        | [5]  | 公有字段数量                                |
| privateFieldsQty       | [5]  | 私有字段数量                                |
| protectedFieldsQty     | [5]  | 保护字段数量                                |
| staticFieldsQty        | [5]  | 静态字段数量                                |
| defaultFieldsQty       | [5]  | 缺省字段数量                                |
| finalFieldsQty         | [5]  | final字段数量                               |
| synchronizedFieldsQty  | [5]  | synchronized字段数量                        |
| RFC                    | [5]  | 类的响应数量(本地方法数量+调用外部方法数量) |
| NOF                    | [5]  | 字段数量                                    |
| NOVM                   | [5]  | 可见方法数量                                |
| NOSI                   | [5]  | 静态方法调用数量                            |
| TCC                    | [5]  | 紧类内聚(仅考虑可见方法的直接调用)          |
| LCC                    | [5]  | 松类内聚(考虑可见方法的直接调用和间接调用)  |
| LCOM                   | [5]  | 方法内聚性缺失                              |
| LOCM*                  | [5]  | 方法内聚性缺失(标准化结果)                  |
| WMC                    | [5]  | 类方法复杂度之和                            |
| c_modifiers            | [5]  | 类中修饰符                                  |

- ### method

| 指标                           | 来源 | 说明                          |
| ------------------------------ | ---- | ----------------------------- |
| startLine                      | ours | 方法开始位置                  |
| CBM                            | [5]  | 方法依赖的数量(call/override) |
| m_FAN_IN                       | [5]  | 方法扇入                      |
| m_FAN_OUT                      | [5]  | 方法扇出                      |
| IDMC                           | [4]  | 模块内耦合方法的数量          |
| EDMC                           | [4]  | 模块外耦合方法的数量          |
| methodsInvokedQty              | [5]  | 调用方法的数量                |
| methodsInvokedLocalQty         | [5]  | 调用本地方法的数量            |
| methodsInvokedIndirectLocalQty | [5]  | 间接调用本地方法的数量        |
| m_variablesQty                 | [5]  | 方法中变量数量                |
| parametersQty                  | [5]  | 方法参数数量                  |
| m_modifier                     | [5]  | 方法修饰符                    |

## 输出结果说明

1  度量功能

输出json格式度量结果，示例如下：
![img.png](./image/measure_result.png)

2  对比功能

输出json格式文件，对两个版本演化过程中每个指标的变化幅度进行统计输出，示例如下：
![img.png](./image/diff.png)

输出xlsx格式文件，其中包含一个演化趋势sheet页，对两个版本在演化过程中的指标变化幅度进行归一化处理，并根据演化的趋势进行指示(越绿代表演化状态越好，越红代表演化状态越差)，示例如下：
![img.png](./image/hotmap.png) 

## 参考文献

[1] C. Zhong, S. Li, H. Zhang, and C. Zhang, “Evaluating granularity of microservices-oriented system based on bounded context,” Journal of Software, vol. 30, no. 10, pp. 3227–3241, 2019.

[2] W. Jin, D. Zhong, Y. Zhang, M. Yang, and T. Liu, “Microservice maintainability measurement based on multi-sourced feature space,”Journal of Software, vol. 32, no. 5, pp. 1322–1340, 2021.

[3] L. L. Silva, M. T. Valente, and M. d. A. Maia, “Assessing modularity using co-change clusters,” in Proceedings of the 13th international conference on Modularity, pp. 49–60, 2014.

[4] J. Bansiya and C. G. Davis, “A hierarchical model for object-oriented design quality assessment,” IEEE Transactions on software engineering,vol. 28, no. 1, pp. 4–17, 2002.

[5] S. R. Chidamber and C. F. Kemerer, “A metrics suite for object oriented design,” IEEE Transactions on software engineering, vol. 20, no. 6, pp. 476–493, 1994.
