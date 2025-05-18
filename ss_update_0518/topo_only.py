#!/usr/bin/env python3
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import Node, Switch
from mininet.cli import CLI

class DummySwitch(Switch):
    # disable Mininet openswitch
    def start(self, controllers): pass
    def stop(self): pass

class SpreadSketchTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1', cls=DummySwitch)
        s2 = self.addSwitch('s2', cls=DummySwitch)
        s3 = self.addSwitch('s3', cls=DummySwitch)

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        self.addLink(h1, s1)
        self.addLink(s1, s2)
        self.addLink(s2, h2)
        self.addLink(s1, s3)
        self.addLink(s3, h3)

if __name__ == '__main__':
    net = Mininet(topo=SpreadSketchTopo(), link=TCLink, controller=None, build=True, autoSetMacs=True)
    net.start()
    
    CLI(net)
    net.stop()

