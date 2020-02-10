
import numbers
import random
import pandas as pd
import pulp as plp

regions = {}
regions['F'] = ['Detorid', 'Cache', 'Insmother', 'Impass', 'Feythabolis', 'Tenerifis', 'Omist']
regions['G'] = ['Stain', 'Esoteria', 'Querious', 'Paragon Soul', 'Delve',' Period Basis']
regions['H'] = ['Vale of the Silent', 'Tribute', 'Venal', 'Geminate', 'Deklein', 'Tenal', 'Branch']
regions['I'] = ['Wicked Creek', 'Scalding Pass', 'Great Wildlands', 'Curse', 'Catch', 'Immensea', 'Providence']
regions['J'] = ['Pure Blind', 'Syndicate', 'Fade', 'Cloud Ring', 'Outer Ring', 'Fountain']
regions['K'] = ['Cobalt Edge', 'Perrigen Falls', 'Malpais', 'Oasa', 'Kalevala Expanse', 'Outer Passage', 'Etherium Reach', 'The Spire']

class Options():
    only_compressed = False
    sucurity_space = ""
    def __init__(self):
        pass

    def add_regions(self, r):
        for region in regions:
            if r in regions[region] and region not in self.sucurity_space:
                if len(self.sucurity_space) > 0:
                    self.sucurity_space += '|' + region
                else:
                    self.sucurity_space += region


class Market_Prices():
    def _set_mineral_price(self):
        pass

reprocessing_methods = {'Single': 'Single', 'Dict': 'Dict'}
Ore_Types = [   'Veldspar',
                'Scordite', 
                'Pyroxeres', 
                'Plagioclase', 
                'Omber', 
                'Kernite', 
                'Jaspet',
                'Hemorphite',
                'Hedbergite',
                'Gneiss',
                'Dark Ochre',
                'Spodumain',
                'Crokite',
                'Bistot',
                'Arkonor',
                'Mercoxit']
Mineral_Types = [   'Tritanium',
                    'Pyerite',
                    'Mexallon',
                    'Isogen',
                    'Nocxium',
                    'Megacyte',
                    'Zydrine',
                    'Morphite']
class Reprocessing():
    _reprocessing_method = None
    _reprocessing_value = None
    def set_reprocessing(self, obj, default=None):
        """[summary]
        
        Arguments:
            obj {Float} -- Reprocessing value to be used for all ore types
            obj {Dict} -- Dictionary of reprocessing values, {'ore type': value}
            obj {TBD} -- [description]            
        
        Keyword Arguments:
            default {Float} -- Reprocessing value to be used if 'obj' does not define a value
        """    
        # Catch if all attributes are None
        if obj == None and default == None:
            raise TypeError("Attributes obj and default were both None.")
        # Carch of default is not None or Float
        if (default != None) and not isinstance(default, numbers.Number):
            raise TypeError("default should be None or float.")

        # Catch case where default is used instead of obj
        if obj == None and isinstance(default, numbers.Number):
            self._reprocessing_method = reprocessing_methods['Single']
            self._reprocessing_value = obj
        # Define for 'Single' case
        elif isinstance(obj, numbers.Number):
            self._reprocessing_method = 'Single'
            self._reprocessing_value = obj
        elif isinstance(obj, dict):
            pass #TODO: 
    
    def get_reprocessing(self):
        """Get reprocessing values      
        
        Returns:
            [Dict{'ore_type': reprocessing_value}] -- Dictionary of reprocessing values for each ore type
        """        
        if self._reprocessing_method == None:
            raise RuntimeError("set_reprocessing has not been successfully completed")
        
        if self._reprocessing_method == reprocessing_methods['Single']:
            return {ore_type : self._reprocessing_value for ore_type in Ore_Types }
        elif self._reprocessing_method == reprocessing_methods['Dict']:
            return self._reprocessing_value

class Minerals():
    _mineral_constraints = None
    def __init__(self):
        self._mineral_constraints = {min_type : None for min_type in Mineral_Types}
        
    
    def set_mineral_constraints(self, min_constraints):
        """[summary]
        
        Arguments:
            obj {list[float]} -- List of mineral constraints. User with caution, expects mineral order
                Tritanium, Pyerite, Mexallon, Isogen, Nocxium, Megacyte, Zydrine, Morphite
            obj {list[tuple['mineral type',float]]} -- List of mineral constraints 
            obj {dict['mineral type',float]} -- Dict of mineral constraints
        """        

        # Parse list
        if isinstance(min_constraints, list):
            if len(min_constraints) != len(min_constraints):
                raise ValueError("min_constraints is of type list but wrong length. Expects len(min_constraints)==8")
            
            if isinstance(min_constraints[0], numbers.Number): # Parse list[float]
                self._mineral_constraints = {Mineral_Types[i] : min_constraints[i] for i in range(len(min_constraints)) }
            elif isinstance(min_constraints[0], tuple): # Parse list[tuple('min type', float)]
                self._mineral_constraints = {item[0] : item[1] for item in min_constraints}
            else:          
                raise ValueError("min_constraints is of type list but items are of wrong type. Expects float or typle(['min_type'], float)")
            
        # Parse dict
        elif isinstance(obj, dict):
            pass
    
    def get_mineral_constraints(self):
        return self._mineral_constraints
