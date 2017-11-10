import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles

### INNER JOIN
plt.figure(0)
s = (1, 1.5, 1)
v = venn2(subsets=s, set_labels=('A', 'B'))
v.get_label_by_id('10').set_text(r' ')
v.get_label_by_id('01').set_text(r'$7$')
v.get_label_by_id('11').set_text(r'$0$, $2$')

c = venn2_circles(subsets=s, linestyle='solid')

### LEFT OUTER JOIN
plt.figure(1)
s1 = (1, 1.5, 1)
v1 = venn2(subsets=s, set_labels=('A', 'B'))
v1.get_label_by_id('10').set_text(r' ')
v1.get_label_by_id('01').set_text(r'$7$')
v1.get_label_by_id('11').set_text(r'$0$, $2$')

v1.get_patch_by_id('10').set_color('g')
v1.get_patch_by_id('01').set_color('w')
v1.get_patch_by_id('11').set_color('g')

#v1.get_patch_by_id('10').set_alpha(0.4)
#v1.get_patch_by_id('01').set_alpha(0.4)
#v1.get_patch_by_id('11').set_alpha(0.4)

c1 = venn2_circles(subsets=s1, linestyle='solid')

plt.show()
