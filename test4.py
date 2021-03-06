import grl
from examples import SlipperyHill

p = grl.Storage(3, default=0.0, leaf_keys=[0,1])
r = grl.Storage(3, default=0.0, leaf_keys=[0,1])

pmin = 0.001
eps_vect = [0.0, -0.00003162277, -0.00001, -0.000003162277, -0.000001]
p_h_vect = [0.5, 0.001, 0.999]

r_sa = grl.Storage(2, default=0.0, leaf_keys=['up', 'stay', 'down'])

theta = 0.999

r_sa[0]['up'] = 0.5
r_sa[0]['stay'] = 0.0
r_sa[0]['down'] = 0.0

r_sa[1]['up'] = 0.0
r_sa[1]['stay'] = 1.0
r_sa[1]['down'] = 0.0

r_s = grl.Storage(1, default=0.0, leaf_keys=[0,1])
f = grl.Storage(2, default=0.0, leaf_keys=['up', 'stay', 'down'])

r_s[0] = r_sa[0].max()
r_s[1] = r_sa[1].max()


for eps in eps_vect:
    v_base = None
    print('Evaluating eps={}'.format(eps))
    for p_h in p_h_vect:
       
        p[0]['up'][1] = p_h
        p[0]['up'][0] = 1.0 - p[0]['up'][1]
        p[0]['down'][0] = 1.0
        p[0]['stay'][0] = 1.0

        p[1]['up'][0] = 1.0
        p[1]['down'][0] = 1.0
        p[1]['stay'][1] = p_h
        p[1]['stay'][0] = 1.0 - p[1]['stay'][1]

        for s in [0,1]:
            for a in ['up', 'down', 'stay']:
                for s_next in [0,1]:
                    #r[s][a][s_next] = (r_sa[s][a]/r_s.avg(p[s][a]) - theta)*r_s[s_next]
                    #r[s][a][s_next] = theta + (1-theta)*r_sa[s][a] - theta*r_s[s_next]
                    #r[s][a][s_next] = r_sa[s][a] + theta*(1 - r_s.avg(p[s][a]))
                    #r[s][a][s_next] = r_sa[s][a] - theta*r_s.avg(p[s][a])
                    #r[s][a][s_next] = (r_sa[s][a] + theta*(1 - r_s.avg(p[s][a])))/(1+theta)
                    #r[s][a][s_next] = ((1-theta)*r_sa[s][a] - theta) * r_s[s_next]
                    f[s][a] = (r_sa[s][a] / r_s.avg(p[s][a]) - theta)/(1-theta)
                    r[s][a][s_next] = f[s][a] * r_s[s_next]


        pi, v = grl.PITabular(p, r, g=theta+eps, normalize=False)

        if v_base is None:
            print('Base @{} : '.format(p_h))
            print(v)
            print(pi)
            v_base = v
        else:
            print('Error @{}'.format(p_h))
            print(v-v_base)
            print(pi)


# Evaluating eps=-0.1
# Original @0.999
# {0: 333.1106224801706, 1: 333.4440674605935}
# Base @0.5 :
# {0: 3.1330548691595954, 1: 3.466499758738153}
# {0: {'up': 1}, 1: {'stay': 1}}
# Error @0.001
# {0: 0.16473909381711538, 1: 0.16473952181343687}
# {0: {'up': 1}, 1: {'stay': 1}}
# Error @0.999
# {0: -0.16474368016996754, 1: -0.16474408741685487}
# {0: {'up': 1}, 1: {'stay': 1}}


# Evaluating eps=-0.01
# Original @0.999
# {0: 333.1106224801706, 1: 333.4440674605935}
# Base @0.5 :
# {0: 30.131219373666276, 1: 30.464664345944776}
# {0: {'up': 1}, 1: {'stay': 1}}
# Error @0.001
# {0: 0.1512399632261321, 1: 0.15124045608045833}
# {0: {'up': 1}, 1: {'stay': 1}}
# Error @0.999
# {0: -0.1512852112076537, 1: -0.15128570100670302}
# {0: {'up': 1}, 1: {'stay': 1}}


# Evaluating eps=-0.001
# Original @0.999
# {0: 333.1106224801706, 1: 333.4440674605935}
# Base @0.5 :
# {0: 166.47195062075548, 1: 166.8053956005657}
# {0: {'up': 1}, 1: {'stay': 1}}
# Error @0.001
# {0: 0.08306963469107131, 1: 0.08307013320890633}
# {0: {'up': 1}, 1: {'stay': 1}}
# Error @0.999
# {0: -0.08331866166776081, 1: -0.08331915898730813}
# {0: {'up': 1}, 1: {'stay': 1}}


# Evaluating eps=-0.0001
# Original @0.999
# {0: 333.1106224801706, 1: 333.4440674605935}
# Base @0.5 :
# {0: 302.8126818697831, 1: 303.14612685034444}
# {0: {'up': 1}, 1: {'stay': 1}}
# Error @0.001
# {0: 0.014900309200470474, 1: 0.0149008071811636}
# {0: {'up': 1}, 1: {'stay': 1}}
# Error @0.999
# {0: -0.015352106678165, 1: -0.01535260474770439}
# {0: {'up': 1}, 1: {'stay': 1}}

# x g(10^-x)
# -1	3.466499
# -1.5	10.38281748340
# -2	30.464664
# -2.5	80.2376304175
# -3	166.805395
# -3.5	253.3731607863
# -4	303.14612685
# -4.5	323.227975784
# -5	330.14429135
# -5.5	332.39347419
# -6	333.11112280




# 0.1	3.466499
# 0.03162277	10.38281748340
# 0.01	30.464664
# 0.003162277	80.2376304175
# 0.001	166.805395
# 0.0003162277	253.3731607863
# 0.0001	303.14612685
# 0.00003162277	323.227975784
# 0.00001	330.14429135
# 0.000003162277	332.39347419
# 0.000001	333.11112280