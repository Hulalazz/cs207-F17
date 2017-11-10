import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles

s = (1, 1.5, 1)
v = venn2(subsets=s, set_labels=('A', 'B'))
v.get_label_by_id('10').set_text(r' ')
v.get_label_by_id('01').set_text(r'$7$')
v.get_label_by_id('11').set_text(r'$0$, $2$')

c = venn2_circles(subsets=s, linestyle='solid')
plt.show()
