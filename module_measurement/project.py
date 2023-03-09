import module_measurement.moduleUtil


class Method():
    def __init__(self, method_id, dep_info):
        self.__method = method_id
        self.__dep = dep_info
        self.startLine = 0
        self.CBM = 0
        self.m_FAN_IN = 0
        self.m_FAN_OUT = 0
        self.IDMC = 0
        self.EDMC = 0
        self.methodsInvokedQty = 0
        self.methodsInvokedLocalQty = 0
        self.methodsInvokedIndirectLocalQty = 0
        self.m_variablesQty = 0
        self.parametersQty = 0
        self.m_modifier = 0
        self.storage_class = ''


class Class():
    def __init__(self, cur_class, class_contain, dep_info):
        self.__methods = class_contain[cur_class]
        self.__dep = dep_info
        self.c_chm = 0
        self.c_chd = 0
        self.CBC = 0
        self.c_FAN_IN = 0
        self.c_FAN_OUT = 0
        self.IDCC = 0
        self.IODD = 0
        self.IIDD = 0
        self.EDCC = 0
        self.NOP = 0
        self.NAC = 0
        self.NDC = 0
        self.NOI = 0
        self.NOID = 0
        self.RFC = 0
        self.NOSI = 0
        self.CTM = 0
        self.c_variablesQty = 0
        self.NOM = 0
        self.WMC = 0
        self.privateMethodsQty = 0
        self.NOVM = 0
        self.CIS = 0
        self.protectedMethodsQty = 0
        self.synchronizedMethodsQty = 0
        self.NOF = 0
        self.publicFieldsQty = 0
        self.privateFieldsQty = 0
        self.protectedFieldsQty = 0
        self.staticFieldsQty = 0
        self.defaultFieldsQty = 0
        self.finalFieldsQty = 0
        self.synchronizedFieldsQty = 0
        self.TCC = 0
        self.LCC = 0
        self.LCOM = 0
        self.LOCM1 = 0
        self.c_modifiers = 0
        self.methods = dict()
        self.__set_methods()

    def __set_methods(self):
        for met in self.__methods:
            self.methods[met] = Method(met, self.__dep)


class Module:
    def __init__(self, cur_module, module_contain, dep_info):
        self.__classes = module_contain[cur_module]
        self.__dep = dep_info
        self.scoh = 0
        self.scop = 0
        self.odd = 0
        self.idd = 0
        self.spread = 0
        self.focus = 0
        self.icf = 0
        self.ecf = 0
        self.rei = 0
        self.chm = 0
        self.chd = 0
        self.DSM = 0
        self.NOI = 0
        self.NOID = 0
        self.classes = dict()
        self.__set_classes()

    def __set_classes(self):
        for cla in self.__classes:
            self.classes[cla] = Class(cla, self.__classes, self.__dep)


class Project:
    def __init__(self, pro_info):
        self.version = pro_info['version']
        self.__contain = pro_info['contain']
        self.__dep = pro_info['dep']
        self.score = 0
        self.SMQ = 0
        self.ODD = 0
        self.IDD = 0
        self.SPREAD = 0
        self.FOCUS = 0
        self.ICF = 0
        self.ICF = 0
        self.ECF = 0
        self.REI = 0
        self.CHM = 0
        self.CHD = 0
        self.modules = dict()
        self.__set_modules()
        self.__set_others()
        # __set_score(self.)

    def __set_modules(self):
        for mod in self.__contain:
            self.modules[mod] = Module(mod, self.__contain, self.__dep)

    def __set_others(self):
        pass







