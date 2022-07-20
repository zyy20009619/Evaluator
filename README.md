# MicroEvaluator工具介绍

## 功能

- 根据项目依赖文件度量项目质量

     ```python
     python measure.py -d [dep_path]   #以package为粒度计算
     python measure.py -d [dep_path] -mp [mpmapping_path]   #以用户定义的粒度计算
     ```

+ 对度量结果进行对比

```python
python measure.py -c1 [com_path1] -c2 [com_path2]    #对两个不同版本的度量结果进行对比(以最新版本的度量结果为基准)
python measure.py -c1 [com_path1] -c2 [com_path2] -pp [ppmapping_path]    #若新版本中的package name有变动，给出变动映射
```

package name映射文件格式示例：

![image-20220314102614421](image\ppmapping.png)

#根据指标变化情况定位问题实体



## 命令说明

 ```python
 -h, --help                            show this help message and exit
 -d DEP, --dep DEP                     dependency file path
 -mp MPMAPPING, --mpmapping MPMAPPING  mapping between module and packages
 -pp PPMAPPING, --ppmapping PPMAPPING  mapping between old package name and new package name
 -c1 COM1, --com1 COM1                 the measure result path of the previous version
 -c2 COM2, --com2 COM2                 the measure result path of the later version
 ```

## 使用步骤

1 解压工具包

2 在工具包路径下运行相应命令

## 指标说明

<table>
   <tr>
      <th>指标</th>
      <th>含义</th>
      <th>粒度</th>
   </tr>
   <tr>
      <td>scoh(structural cohesion)</td>
      <td>结构内聚度</td>
      <td>module</td>
   </tr>
   <tr>
      <td>scop(structural coupling)</td>
      <td>结构耦合度</td>
      <td>module</td>
   </tr>
   <tr>
      <td>odd(out-degree dependence)</td>
      <td>耦合其他模块程度</td>
      <td>module</td>
   </tr>
   <tr>
      <td>idd(in-degree dependence)</td>
      <td>被其他模块耦合程度</td>
      <td>module</td>
   </tr>
   <tr>
      <td>DSM(design size in module)</td>
      <td>模块中类总数</td>
      <td>module</td>
   </tr>
   <tr>
      <td>CBC(Coupling between classes)</td>
      <td>类依赖的数量(包含被依赖)</td>
      <td>class</td>
   </tr>
    <tr>
      <td>IDCC(intra direct class coupling)</td>
      <td>模块内耦合类数量</td>
      <td>class</td>
   </tr>
    <tr>
      <td>EDCC(external direct class coupling)</td>
      <td>模块外耦合类数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>c_FAN_IN</td>
      <td>类扇入</td>
      <td>class</td>
   </tr>
   <tr>
      <td>c_FAN_OUT</td>
      <td>类扇出</td>
      <td>class</td>
   </tr>
   <tr>
      <td>NAC(Number of Ancestor Classes)</td>
      <td>类继承树深度</td>
      <td>class</td>
   </tr>
   <tr>
      <td>NDC(Number of Descendent Classes)</td>
      <td>派生类个数</td>
      <td>class</td>
   </tr>
   <tr>
      <td>NOP(number of polymorphic methods)</td>
      <td>多态方法数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>RFC(Response for a Class)</td>
      <td>类的响应集数量(调用本地方法数量+调用外部方法数量)</td>
      <td>class</td>
   </tr>
   <tr>
      <td>NOSI(Number of static invocations)</td>
      <td>静态方法调用数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>CTM(Coupling through Message Passing)</td>
      <td>调用方法个数(除本地方法)</td>
      <td>class</td>
   </tr>
   <tr>
      <td>NOM(number of methods)</td>
      <td>类中方法总数</td>
      <td>class</td>
   </tr>
   <tr>
      <td>NOVM(Number of visible methods)</td>
      <td>可见方法数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>CIS(Class interface size)</td>
      <td>类中公共接口数</td>
      <td>class</td>
   </tr>
   <tr>
      <td>privateMethodsQty</td>
      <td>私有方法数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>protectedMethodsQty</td>
      <td>保护方法数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>staticMethodsQty</td>
      <td>静态方法数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>defaultMethodsQty</td>
      <td>缺省方法数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>abstractMethodsQty</td>
      <td>抽象方法数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>finalMethodsQty</td>
      <td>final方法数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>synchronizedMethodsQty</td>
      <td>synchronized方法数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>TCC(Tight Class Cohesion)</td>
      <td>紧类内聚(仅考虑可见方法的直接调用)</td>
      <td>class</td>
   </tr>
   <tr>
      <td>LCC(Loose Class Cohesion)</td>
      <td>松类内聚(考虑可见方法的直接调用和间接调用)</td>
      <td>class</td>
   </tr>
   <tr>
      <td>LCOM(Lack of Cohesion of Methods)</td>
      <td>方法内聚性缺失</td>
      <td>class</td>
   </tr>
   <tr>
      <td>LCOM*(Lack of Cohesion of Methods)</td>
      <td>方法内聚性缺失(标准化结果)</td>
      <td>class</td>
   </tr>
   <tr>
      <td>WMC(Weight Method Per Class)</td>
      <td>类方法权重(每个方法给予1个复杂度)</td>
      <td>class</td>
   </tr>
   <tr>
      <td>c_variablesQty</td>
      <td>类中变量数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>NOF(Number of fields)</td>
      <td>字段数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>publicFieldsQty</td>
      <td>公有字段数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>privateFieldsQty</td>
      <td>私有字段数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>protectedFieldsQty</td>
      <td>保护字段数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>staticFieldsQty</td>
      <td>静态字段数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>defaultFieldsQty</td>
      <td>缺省字段数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>finalFieldsQty</td>
      <td>final字段数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>synchronizedFieldsQty</td>
      <td>synchronized字段数量</td>
      <td>class</td>
   </tr>
   <tr>
      <td>c_modifiers</td>
      <td>类修饰符</td>
      <td>class</td>
    </tr>
   <tr>
      <td>startLine</td>
      <td>方法开始位置</td>
      <td>method</td>
   </tr>
   <tr>
      <td>CBM(Coupling between methods)</td>
      <td>方法依赖的数量(包含被依赖)</td>
      <td>method</td>
   </tr>
   <tr>
      <td>IDMC</td>
      <td>模块内耦合方法的数量</td>
      <td>method</td>
   </tr>
   <tr>
      <td>EDMC</td>
      <td>模块外耦合方法的数量</td>
      <td>method</td>
   </tr>
   <tr>
      <td>m_FAN_IN</td>
      <td>方法扇入</td>
      <td>method</td>
   </tr>
   <tr>
      <td>m_FAN_OUT</td>
      <td>方法扇出</td>
      <td>method</td>
   </tr>
   <tr>
      <td>methodsInvokedQty</td>
      <td>调用方法的数量</td>
      <td>method</td>
   </tr>
   <tr>
      <td>methodsInvokedLocalQty</td>
      <td>调用本地方法的数量</td>
      <td>method</td>
   </tr>
   <tr>
      <td>methodsInvokedIndirectLocalQty</td>
      <td>间接调用本地方法的数量</td>
      <td>method</td>
   </tr>
   <tr>
      <td>m_variablesQty</td>
      <td>方法中变量数量</td>
      <td>method</td>
   </tr>
   <tr>
      <td>parametersQty</td>
      <td>方法参数数量</td>
      <td>method</td>
   </tr>
   <tr>
      <td>m_modifiers</td>
      <td>方法修饰符</td>
      <td>method</td>
   </tr>
</table>



## 输出结果说明

1  度量功能

输出json格式度量结果，示例如下：
![img.png](image/measure_result.png)

2  对比功能

输出json格式文件，对两个版本演化过程中每个指标的变化幅度进行统计输出，示例如下：
![img.png](image/diff.png)

输出xlsx格式文件，其中包含一个演化趋势sheet页，对两个版本在演化过程中的指标变化幅度进行归一化处理，并根据演化的趋势进行指示(越绿代表演化状态越好，越红代表演化状态越差)，示例如下：
![img.png](image/hotmap.png)
