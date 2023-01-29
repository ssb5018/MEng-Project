from ..constraints.constraints import Constraints
from .hyperparameters import Hyperparameters
from ..motif_generation_tool.key_payload_builder import KeyPayloadBuilder

import numpy as np
import time
import os

class HyperparameterTuning:
    def __init__(self, number_of_runs=100):
        self.number_of_runs = number_of_runs

    async def build_keys_and_payloads(self, constraints, hyperparameters, with_constraints):
        keyPayloadBuilder = KeyPayloadBuilder(constraints, hyperparameters)
        keys, payloads = await keyPayloadBuilder.build_keys_and_payloads(with_constraints)
        return keys, payloads
    
    async def round_validation(self, constraints, hyperparameters, with_constraints):
        keys, payloads = await self.build_keys_and_payloads(constraints, hyperparameters,\
                                                            with_constraints)
        if not (keys and payloads):
            return False
        return True

    async def round(self, constraints, hyperparameters, with_constraints):
        totalSuccesses = 0
        for i in range(self.number_of_runs):
            valid = await self.round_validation(constraints, hyperparameters, with_constraints)
            totalSuccesses += 1 if valid else 0
        return totalSuccesses
    
    async def grid_search(self, constraints, shape_values, weight_values, with_constraints):
        """This function takes a set of possible hyperparameter values and tries out all
        of their combinations. It stores the results in the file hypTun.txt.
        
        Parameters
        ----------
        shape_values: dict str: list int/float
            Dictionary of constraints to the values we want to try the shape hyperparameters 
            corresponding to each constraint for. Constraints are 'hairpin', 'hom', 'similarity',
            'gcContent'.
        weight_values: dict str: list int/float
            Dictionary of constraints to the values we want to try the weight hyperparameters 
            corresponding to each constraint for. Constraints are 'hairpin', 'hom', 'similarity',
            'gcContent'.
        with_constraints: set of str
            Set of strings containing a selection of the following constraints: 
            'hairpin', 'hom', 'gcContent'. Those will be the constraints that the
            palyoads and keys will have to conform to.
        """

        hom_shapes = [1] if not 'hom' in shape_values else shape_values['hom']
        hairpin_shapes = [1] if not 'hairpin' in shape_values else shape_values['hairpin']
        similarity_shapes = [1] if not 'similarity' in shape_values else shape_values['similarity']
        gc_shapes = [1] if not 'gcContent' in shape_values else shape_values['gcContent']

        hom_weights = [1] if not 'hom' in weight_values else weight_values['hom']
        hairpin_weights = [1] if not 'hairpin' in weight_values else weight_values['hairpin']
        similarity_weights = [1] if not 'similarity' in weight_values \
                                 else weight_values['similarity']
        gc_weights = [1] if not 'gcContent' in weight_values else weight_values['gcContent']

        for hom_shape in hom_shapes:
            for hom_weight in hom_weights:
                for hairpin_shape in hairpin_shapes:
                    for hairpin_weight in hairpin_weights:
                        for similarity_shape in similarity_shapes:
                            for similarity_weight in similarity_weights:
                                for gc_shape in gc_shapes:
                                    for gc_weight in gc_weights:
                                        shapes = {'hom': hom_shape, 
                                                  'hairpin': hairpin_shape, 
                                                  'similarity': similarity_shape,
                                                  'gcContent': gc_shape 
                                                  }
                                        weights = {'hom': hom_weight, 
                                                   'hairpin': hairpin_weight, 
                                                   'similarity': similarity_weight,
                                                   'gcContent': gc_weight 
                                                   }
                                        hyp = Hyperparameters(shapes, weights)
                                        start = time.time()
                                        total_successes = await self.round(constraints, hyp, \
                                                                            with_constraints)
                                        end = time.time()
                                        print('time: ', end - start)
                                        print('total successes: ', total_successes)
                                        w = 'weights: ' + str(weights) + 'shapes: ' + str(shapes) + \
                                            'totalSuccesses: ' + str(total_successes) + '\n'
                                        f = open(os.path.join(os.path.dirname(__file__), "hypTun.txt"), "a")
                                        f.write(w)
                                        f.close()


async def main():
    payload_size = 60
    payload_num = 15
    max_hom = 5
    max_hairpin = 1
    loop_size_min = 6
    loop_size_max = 7
    min_gc = 25
    max_gc = 65
    key_size = 20
    key_num = 8
    
    constraints = Constraints(payload_size=payload_size, payload_num=payload_num, max_hom=max_hom, \
                              max_hairpin=max_hairpin, min_gc=min_gc, max_gc=max_gc, \
                              key_size=key_size, key_num=key_num, loop_size_min=loop_size_min, \
                              loop_size_max=loop_size_max)

    number_of_runs = 1

    hyp_tuning = HyperparameterTuning(number_of_runs)

    shape_values = {'hom': [10, 20, 30, 40, 50], \
                    'hairpin': [10, 20, 30, 40, 50], \
                    'similarity': [10, 20, 30, 40, 50], \
                    'gcContent': [10, 20, 30, 40, 50]
                    }
    weight_values = {'hom': [1, 2, 3, 4, 5], \
                     'hairpin': [1, 2, 3, 4, 5], \
                     'similarity': [1, 2, 3, 4, 5], \
                     'gcContent': [1, 2, 3, 4, 5]
                    } 
    with_constraints = {'hom', 'hairpin', 'gcContent'}
    await hyp_tuning.grid_search(constraints, shape_values, weight_values, with_constraints)
    
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())


    