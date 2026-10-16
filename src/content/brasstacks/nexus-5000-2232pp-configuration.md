---
title: "Nexus 5000 / 2232PP configuration"
pubDate: 2010-11-04
postedAt: "03:29 PM"
description: "As I’ve mentioned in my previous posts, I work for the Connectivity team in EMC’s E-Lab. Our primary responsibility is to set up configurations that our customers are likely to use, enable many of the more useful features and then see what kind of trouble we can cause by performing..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2010/11/nexus-5000-2232pp-configuration.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250911143804/https://brasstacksblog.typepad.com/brass-tacks/2010/11/nexus-5000-2232pp-configuration.html"
pdf: "/brasstacks/nexus-5000-2232pp-configuration/nexus-5000-2232pp-configuration.pdf"
comments:
  - author: "Anthony Padula"
    date: "11/05/2010 at 09:41 PM"
    html: |-
      <p>Quick question Erik, do you know when we will be able to uplink the 5020 to an MDS using NPV and port channels?</p>
      <p>I notice in your example you have used TE-ports, but I&#39;d like to have a trunked NP-port instead.</p>
  - author: "Erik Smith"
    date: "11/06/2010 at 12:03 AM"
    html: |-
      <p>Hi Anthony, great question.  Cisco is referring to this as F_Port Channeling and it is supported as of NX-OS 4.2(1)N1(1).  I&#39;ll update the topology and add the setup steps to the FCoE tech book.  Hopefully I&#39;ll be able to get it into the December release.</p>
      <p>Erik </p>
  - author: "Anthony Padula"
    date: "11/07/2010 at 07:42 PM"
    html: |-
      <p>That&#39;s great, do you know if the same thing applies to the UCS 61x0XP&#39;s?</p>
---

<p>As I’ve mentioned in my previous posts, I work for the Connectivity team in EMC’s E-Lab.&#0160; Our primary responsibility is to set up configurations that our customers are likely to use, enable many of the more useful features and then see what kind of trouble we can cause by performing disruptive tests like cable pulls, inserting errors with a jammer, switch reboots during I/O, etc.&#0160; After I complete a round of testing, I know I’ve done a good job if I’ve found an error condition that a device can’t recover from.&#0160;&#0160;&#0160;&#0160;</p>
<p>Once a configuration is set up and we’re satisfied that it’s operating correctly, we document exactly what we tested as well as any test results and caveats.&#0160; If the configuration contains a new piece of technology, we create a new case study that will be published in the <a href="http://www.emc.com/collateral/hardware/technical-documentation/h6290-fibre-channel-over-ethernet-techbook.pdf" target="_self" title="FCoE Tech book">FCoE Tech book</a>.&#0160; We publish this information so our customers will be able to get a particular piece of equipment into production with as little frustration as possible.&#0160; The idea is, if a customer has a miserable time installing something or installs it incorrectly, all of the work done to ensure that the device is as robust as possible won’t provide much value.&#0160;</p>
<p>I mention all of this because we recently added a new case study that shows how to incorporate the Nexus 2232PP into an FCoE environment.&#0160; The configuration that was set up and tested is shown below.</p>
<p><a href="/brasstacks/nexus-5000-2232pp-configuration/6a013487ed263f970c0133f5969394970b.jpg" style="display: inline;"><img alt="5000-2232-novpc" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0133f5969394970b image-full" src="/brasstacks/nexus-5000-2232pp-configuration/6a013487ed263f970c0133f5969394970b.jpg" title="5000-2232-novpc" /></a>&#0160;</p>
<p>The step-by-step instructions for setting up this topology are documented in the EMC <a href="http://www.emc.com/collateral/hardware/technical-documentation/h6290-fibre-channel-over-ethernet-techbook.pdf" target="_self" title="FCoE Tech book">FCoE tech book</a>, so I will not repeat them here.&#0160; However, it may be helpful to provide a brief overview of the topology components, summarize the setup steps and then discuss some of the caveats specific to this topology.&#0160;</p>
<p><strong>Topology elements:</strong></p>
<p>The topology consists of (2) Nexus 5020s, (2) Nexus 2232PP Fabric Extenders, a host with a dual ported CNA, (2) different FC SANs and a LAN.</p>
<p><strong>Nexus 5020:</strong></p>
<p>The Nexus 5020 is Cisco’s 10GbE switch that also happens to contain a Fibre Channel Forwarder (FCF).&#0160; As you would expect, there is a ton of information on Cisco’s website that covers every aspect of the 5020 in detail.&#0160; One of the more interesting documents covers the <a href="http://www.cisco.com/en/US/prod/collateral/switches/ps9441/ps9670/white_paper_c11-462176.pdf" target="_self" title="Nexus 5000 architecture">Nexus 5000 architecture</a>.&#0160; In the above topology, each Nexus 5020 is connected to a different SAN in order to maintain EMC’s SAN A / SAN B best practice for redundancy.&#0160; The link between one of the Nexus 5020s and the Cisco SAN consists of TE_Ports and these ports are part of a SAN Port Channel.&#0160; The 5020 connected to the Brocade switch is in NPV mode.&#0160; Each 5020 is also connected to the LAN allowing for the non-FCoE frames to be forwarded to their ultimate destination.&#0160;</p>
<p><strong>Nexus 2232PP:</strong></p>
<p>The Nexus 2232PP is Cisco’s Fabric Extender (FEX) product.&#0160; Again there is a ton of information available on Cisco’s website for this product.&#0160; A few interesting points about the 2232PP include:</p>
<ul>
<li>It’s managed from the Nexus 5000 that it’s connected to.&#0160; In other words interface display, configuration, etc is done from the 5000.</li>
<li>Firmware is automatically downloaded to it from the 5000.</li>
<li>It does not perform any local switching.&#0160; All frames are forwarded to the Nexus 5000 it is attached to before a forwarding decision is made.&#0160; Given the actual topologies that the Nexus 2232PP is used in, I don’t see this as being a huge problem.&#0160; (Note: I plan to cover realistic FCoE topologies in the near future)</li>
<li>Worst case oversubscription is 4:1&#0160; </li>
<li>It uses NIV.&#0160; <a href="http://blog.scottlowe.org/2010/03/16/understanding-network-interface-virtualization" target="_self" title="NIV overview">Scott Lowe has done an outstanding job </a>of describing what this technology is and how it works, so I won’t dive into those details here.</li>
<li>It is capable of using lower cost FET (Fabric Extender Transceivers) for connectivity to the Nexus 5000.</li>
<li>It can be simultaneously connected to two Nexus 5000s to create an Active-Active topology but not if you want to use FCoE!&#0160;</li>
</ul>
<p><strong>Host and CNA:</strong></p>
<p>The CNA connections are spread across both 2232PPs to allow for redundancy.&#0160; In our testing, PowerPath was used for failover and load balancing.</p>
<p><strong>Setup steps:</strong></p>
<p>Starting from scratch, the setup steps used to create this topology are summarized as follows:&#0160;</p>
<p><strong>On each 5000 in the topology:</strong></p>
<ol>
<li>Configure the switch management interface, basic settings and password</li>
<li>Enable the FCoE, LACP, FEX, LLDP and NPV (if applicable) features</li>
<li>Create the appropriate VSANs</li>
<li>Create the appropriate VLANs</li>
<li>Create and configure a FEX instance</li>
<li>Create and configure the FEX EtherChannel</li>
<li>Create vFC interfaces and bind them to the ENode MAC of the CNA</li>
<li>Assign each vFC to the appropriate VSAN</li>
<li>Configure Ethernet uplink settings</li>
<li>Add FC interfaces to the appropriate VSAN (if applicable)</li>
<li>Connect cables and verify login</li>
<li>Save the configuration</li>
<li>Perform Fabric zoning</li>
<li>Provision storage</li>
</ol>
<p>Again, for more details refer to the “Nexus 2000 Supported features and topologies” as well as the “Nexus 50x0/Nexus 2232PP Topology” sections of the <a href="http://www.emc.com/collateral/hardware/technical-documentation/h6290-fibre-channel-over-ethernet-techbook.pdf" target="_self" title="FCoE Tech book">FCoE Tech book</a>.</p>
<p><strong>Caveats:</strong></p>
<p>Overall, I found that this configuration works well.&#0160; The complaints I do have center around the need to bind the vFC to the ENode MAC address of the CNA.&#0160; With some CNAs, this can be a relatively straight-forward process that involves opening the CNA Management tool and locating the ENode MAC.&#0160; On others, you will need to take note of both MAC addresses when you are installing the CNA into the server and then bind one of these to the vFC.&#0160; The trick is choosing the correct MAC address because choosing the wrong one will prevent the CNA from successfully logging in!&#0160; I’ve found a couple of different ways to determine the ENode MAC (described below) that work well in the lab, but I would really like it if Cisco would provide a “show mac enode” command to make things simpler.&#0160;&#0160;</p>
<p>&#0160;<strong>How to find the ENode MAC:</strong></p>
<ol>
<li>As I mentioned above, the most reliable way is via the CNAs management tool.&#0160; However, this information is not always available via this method.</li>
<li>Another method is to create a vFC and bind it to a physical interface on the 5000 (i.e. interface ethernet 1/1).&#0160; Next, attach the CNA in question to the interface on the 5000 and use “show fcoe database”.&#0160; Assuming that the CNA logs in, the ENode MAC will be displayed under the MAC Address column.&#0160; You can then bind this MAC Address to the vFC that you actually want to use.</li>
<li>If you took note of both MAC Addresses when you installed the CNA into the host, you can use “show mac address-table” on the 5000.&#0160; The ENode MAC is the MAC Address that is <strong>NOT</strong> shown in this table.&#0160; For example, let’s say that during the installation of the CNA, you record MAC Address A and B.&#0160; Let’s also assume that when you use the “show mac address-table” command on the 5000, MAC Address A is present in the list.&#0160; If this is the case, then MAC Address B is the ENode MAC.</li>
<li>If you didn’t take note of the MAC Address on the CNA before you installed it, and you are unable or unwilling to power down the server, pull the CNA and look at the label, you can always take an educated guess.&#0160; This can be done because all of the CNAs that I am familiar with have the ENode MAC set to be one or two numbers higher or lower than the MAC Address that is displayed via “show mac address-table”.&#0160; For example let’s say that “show mac address-table” shows you a MAC Address of “0000.976f.c16a”, the ENode MAC is going to be one of the following “0010.186f.c168”, “0010.186f.c169”, “0010.186f.c16b” or “0010.186f.c16c”.&#0160; With this knowledge in hand, you can experiment and try each one until you see a valid FCoE login.&#0160; It isn’t pretty but it works in a pinch.&#0160; Also, I advise trying the MAC Address that is one number higher (i.e. 0010.186f.c16b ) first.</li>
</ol>
<p>&#0160;If you made it this far, thanks for reading!&#0160; Hopefully you’ve found it informative and ideally helpful.&#0160; In early December, look for a similar post on Cisco’s vPC feature that provides an alternative to spanning tree and improves both bandwidth and link failover facilities.</p>
