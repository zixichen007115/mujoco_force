import numpy as np
import matplotlib.pyplot as plt

data = np.load('data.npz')
pos = data['pos']
force = data['force']

fig=plt.figure()
ax1=fig.add_subplot(251)
ax2=fig.add_subplot(253)
ax3=fig.add_subplot(255)
ax4=fig.add_subplot(256)
ax5=fig.add_subplot(258)
ax6=fig.add_subplot(2,5,10)

ax1.set_xlabel('time(step)')
ax2.set_xlabel('time(step)')
ax3.set_xlabel('time(step)')
ax4.set_xlabel('time(step)')
ax5.set_xlabel('time(step)')
ax6.set_xlabel('time(step)')

ax1.set_ylabel('force on x axis(N)')
ax2.set_ylabel('force on y axis(N)')
ax3.set_ylabel('force on z axis(N)')
ax4.set_ylabel('displacement on x axis(m)')
ax5.set_ylabel('displacement on y axis(m)')
ax6.set_ylabel('displacement on z axis(m)')

# ax1.plot(force[110*10+0:110*10+110,2])
# ax2.plot(pos[110*10+0:110*10+110,2])

ax1.plot(force[:,0])
ax2.plot(force[:,1])
ax3.plot(force[:,2])
ax4.plot(pos[:,0])
ax5.plot(pos[:,1])
ax6.plot(pos[:,2])

# ax1.plot(force)
# ax2.plot(pos)

plt.show()

