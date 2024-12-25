import os
import tqdm


data = {}
deps = {}


def get_value(a):
    if a['operation']:
        op1 = get_value(data[a['op1']])
        op2 = get_value(data[a['op2']])
        value = globals()[a['value']](op1[0], op2[0])
        return (value, f"({op1[1]} {a['value']} {op2[1]})")
    return (a['value'], a['flat'])


def XOR(a, b):
    return a ^ b


def AND(a, b):
    return a and b


def OR(a, b):
    return a or b

def work2():
    inter = []
    t = {}
    for op in deps['x00']:
        
        if data[op]['value'] == 'XOR':
            t['result'] = op
        elif data[op]['value'] == 'AND':
            t['carry'] = op
        else:
            raise ValueError(f"Unexpected operation: {data[op]['value']} ({data[op]})")
    inter.append(t)    

    for i in range(1, 45):
        t = {}
        for op in deps[f'x{i:02}']:
            if data[op]['value'] == 'XOR':
                t['result_inter'] = op
            elif data[op]['value'] == 'AND':
                t['carry_inter_1'] = op
        carry_prev = inter[-1]['carry']
        
        ops1 = deps[t['result_inter']]
        ops2 = deps[inter[-1]['carry']]
        test_same = sorted(ops1) == sorted(ops2)
        test_z_1 = f'z{i:02}' in ops1
        test_z_2 = f'z{i:02}' in ops2
        test_result = data[f'z{i:02}']['ops'] == set([t['result_inter'], inter[-1]['carry']])
        if ops1[0] == f'z{i:02}':
            t['carry_inter_2'] = ops1[1]
        else:
            t['carry_inter_2'] = ops1[0]
        test_carry = deps[t['carry_inter_2']]
        t['carry'] = test_carry[0]
        if not (test_same and test_z_1 and test_z_2 and test_result and (len(test_carry) == 1)): raise ValueError("Conditions violated") 
        inter.append(t)
        pass
        
def work():
    for k, v in data.items():
        value = get_value(v)
        data[k]['value'] = value[0]
        data[k]['flat'] = value[1]
        data[k]['operation'] = False
    result = {'x': "", 'y': "", 'z': ""}
    for res in ['x', 'y', 'z']:
        for k in sorted([k for k in data.keys() if k[0] == res], reverse=True):
            #print(k, data[k]["flat"])
            result[res] += str(int(data[k]["value"]))
    # print(f'{k}: {int(data[k]["value"])}')
    print(result)
    for res in ['x', 'y', 'z']:
    
        print(result[res])
    print('Part 1:', int(result['z'], 2))
    
    pass
def verify_z(wire, num):
    print("vz", wire, num)
    op, x, y = formulas[wire]
    if op != "XOR": return False
    if num == 0: return sorted([x, y]) == ["x00", "y00"]
    return verify_intermediate_xor(x, num) and verify_carry_bit(y, num) or \
        verify_intermediate_xor(y, num) and verify_carry_bit(x, num)

def make_wire(char, num):
    return f"{char}{num:02}"
def verify_intermediate_xor(wire, num):
    # R_I_num
    print("vx", wire, num)
    op, x, y = formulas[wire]
    if op != "XOR": return False
    return sorted([x, y]) == [f"x{num:02}", f"y{num:02}"]

def verify_carry_bit(wire, num):
    # C_num
    print("vc", wire, num)
    op, x, y = formulas[wire]
    if num == 1:
        return op == "AND" and sorted([x, y]) == ["x00", "y00"]
    if op != "OR": return False
    return verify_direct_carry(x, num - 1) and verify_recarry(y, num - 1) or \
        verify_direct_carry(y, num - 1) and verify_recarry(x, num - 1)

def verify_direct_carry(wire, num):
    # C_I_num
    print("vd", wire, num)
    op, x, y = formulas[wire]
    if op != "AND": return False
    return sorted([x, y]) == [f"x{num:02}", f"y{num:02}"]

def verify_recarry(wire, num):
    # C_II_num
    print("vr", wire, num)
    op, x, y = formulas[wire]
    if op != "AND": return False
    return verify_intermediate_xor(x, num) and verify_carry_bit(y, num) or \
        verify_intermediate_xor(y, num) and verify_carry_bit(x, num)
def verify(num):
    return verify_z(f"z{num:02}", num)
formulas={}
def main():
    # Get the name of the Python script

    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    with open(input_file) as f:
        for line in tqdm.tqdm(f.readlines()):
            line = line.strip()
            if line == '#':
                break
            if line.find(':') >= 0:
                data[line.split(':')[0]] = {
                    'operation': False,
                    'value': bool(int(line.split(':')[1])),
                    'self': line.split(':')[0],
                    'flat': line.split(':')[0]
                    }
            elif line.find('->') >= 0:
                a = line.split(' -> ')
                op1, op, op2 = a[0].split()
                formulas[a[1]] = (op, op1, op2)
                deps[op1] = deps.get(op1,[]) + [a[1]]
                deps[op2] = deps.get(op2,[]) + [a[1]]
                
                data[a[1]] = {
                    'operation': True,
                    'value': op,
                    'op1': op1,
                    'op2': op2,
                    'ops': set([op1, op2]),
                    'self': a[1]
                }
        # work2()
    for i in range(50):
        if not verify(i): break
    print(print(verify(45)))
    # Z15 swapped with QNW
    # z20 swapped with CQR
    # nfj swapped with ncd
    # z37 swapped with vkg


if __name__ == '__main__':
    main()
