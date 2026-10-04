print(f"Error creating curve: {e}") \n return False, None, None, None, None, None,
None, False, None \n \n delta = E.discriminant() \n conductor = E.conductor() \n
tors_order = E.torsion_subgroup().order() \n\n print(f"Discriminant: {delta}") \n
print(f"Conductor: {conductor} = {factor(conductor)}") \n print(f"Torsion order:
