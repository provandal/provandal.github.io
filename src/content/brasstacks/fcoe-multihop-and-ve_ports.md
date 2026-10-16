---
title: "FCoE Multihop and VE_Ports"
pubDate: 2011-03-27
postedAt: "10:16 PM"
description: "In the April EMC Support Matrix, EMC will be posting support for NX-OS 5.0(2)N2(1) for the Nexus 5010, 5020 and 5548. In addition, we will also now support the creation of Virtual E_Ports (VE_Ports) on these products. This post discusses what VE_Ports are, the protocol used to instantiate them and..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2011/03/fcoe-multihop-and-ve_ports.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250910185743/https://brasstacksblog.typepad.com/brass-tacks/2011/03/fcoe-multihop-and-ve_ports.html"
pdf: "/brasstacks/fcoe-multihop-and-ve_ports/fcoe-multihop-and-ve_ports.pdf"
comments:
  - author: "Account Deleted"
    date: "05/09/2011 at 08:23 AM"
    html: |-
      <p>Hi Eric,</p>
      <p>Thank you for such a detailed description, but I am in a fix here. I followed the exact steps given by you for VE port configuration on the cisco nexus. Although on both nexus switches, my vfc&#39;s say it is bound to port-channel 777, port is E and mode is TE.</p>
      <p>They are just not able to talk with each other. What should be the priority-flow-control settings on the port-channel interface?? I have set them to auto/off/on but no luck. The pre-requisite of identical FC-MAPS on both switches is also followed. Following is the VFC output. Note that on both the switches, I added vfc777 only under vsan 2 in the vsan database.</p>
      <p>switch(config-if)# show interface vfc 777<br />
      vfc777 is trunking (Not all VSANs UP on the trunk)<br />
      Bound interface is port-channel777<br />
      Hardware is Virtual Fibre Channel<br />
      Port WWN is 23:08:00:0d:ec:b1:d6:ff<br />
      Admin port mode is E, trunk mode is on<br />
      snmp link state traps are enabled<br />
      Port mode is TE<br />
      Port vsan is 2<br />
      Trunk vsans (admin allowed and active) (2,10,20,200)<br />
      Trunk vsans (up)                       ()<br />
      Trunk vsans (isolated)                 ()<br />
      Trunk vsans (initializing)             (2,10,20,200)<br />
      1 minute input rate 0 bits/sec, 0 bytes/sec, 0 frames/sec<br />
      1 minute output rate 0 bits/sec, 0 bytes/sec, 0 frames/sec<br />
      0 frames input, 0 bytes<br />
      0 discards, 0 errors<br />
      0 frames output, 0 bytes<br />
      0 discards, 0 errors<br />
      last clearing of &quot;show interface&quot; counters never<br />
      Interface last changed at Mon May  9 11:12:26 2011</p>
      <p>Thanks,<br />
      Somu<br />
      </p>
  - author: "Erik Smith"
    date: "05/09/2011 at 12:48 PM"
    html: |-
      <p>Hi Somu, sorry to hear you&#39;re having a tough time.  If you could send me the following output from both switches that you are trying to connect together via the VE_Port, I&#39;ll take a look and see if I can figure out where the problem is.</p>
      <p>show running-config<br />
      show int brief<br />
      show fcoe database<br />
      show int port-channel 777</p>
      <p>You can email them to me at gid_ft@yahoo.com </p>
  - author: "BRCDbreams"
    date: "11/09/2011 at 09:05 PM"
    html: |-
      <p>Erik,</p>
      <p>Do I understand this correctly that the FCoE traffic is separated from the IP traffic on the ISL link?  In short, this is NOT a converged network (FCP + IP over Ethernet), but a separate network physical path for FCoE and a second separate network physical path for IP traffic?</p>
      <p>Thanks.</p>
  - author: "Erik Smith"
    date: "11/10/2011 at 03:46 PM"
    html: |-
      <p>Hi Brook, you&#39;re right.  There are good reasons for this but they&#39;re hard to articulate without sounding like I&#39;ve drowned in the Cisco cool-aid!  :-)</p>
      <p>At first I really didn&#39;t like the idea because it&#39;s not necessary for any protocol related reasons and it messed with the pretty converged network picture I had in my head at the time.  That having been said, the Customers that I&#39;ve spoken with about this actually like the idea of separating FCoE from non-FCoE at the first FCF.  The reason is this approach allows the storage guys to mostly retain control of the SAN while allowing them to take advantage of the economic advantages that FCoE to the ToR allows for.  </p>
      <p>BTW, I&#39;m looking forward to working on VCS, that should be very interesting as well. </p>
      <p>Regards, Erik </p>
  - author: "Bruce"
    date: "01/31/2012 at 10:39 PM"
    html: |-
      <p>G&#39;day Erik,</p>
      <p>Can you confirm if you have tested or implemented 2 x Nexus 5548UP Switches that are connected over distance (40Km) using ISL/E-port&#39;s? Let&#39;s say 1 N5K is in 1 datacentre and the other is in another datentre. We are also going through a CWDM.</p>
      <p>Regards,</p>
      <p>Bruce  </p>
  - author: "Erik Smith"
    date: "02/01/2012 at 08:10 AM"
    html: |-
      <p>Hi Bruce, the maximum distance I&#39;ve tested between 2 5500s was 300m.  </p>
      <p>That having been said, I believe what you are attempting to do won&#39;t work with the 5500s as they don&#39;t have enough buffering to allow PFC to function properly and prevent frame loss due to buffer overrun.  Basically, their high water mark threshold (the point at which they will transmit PFC frame due to a buffer full condition) does not take into account the extra &quot;buffering&quot; taking place on the link.  As a result, they don&#39;t reserve enough space for all of the frames in transit and these frames can be dropped under congestion conditions. </p>
      <p>I believe the Nexus 7k and the FCoE Blade for the MDS will support up to 40km.</p>
      <p>A workaround would be to use FC for the connectivity between the 5548&#39;s.  </p>
  - author: "Sorin"
    date: "06/11/2015 at 01:35 AM"
    html: |-
      <p>I know this is an old post, but maybe i get lucky....<br />
      I have one question: suppose i have a server and a storage fcoe connected to separate 5ks. The 5ks are vonnected by ve ports.<br />
      The fcoe data packets betweek the servers would use source and destination mac as the fcmap, wright? Or both servers would use destination mac addrss as the fcf mac? For me the second one seems more complicated but i can&#39;t find an answer... <br />
      Thanks for the nice post!</p>
  - author: "Erik Smith"
    date: "06/11/2015 at 08:28 AM"
    html: |-
      <p>Hi Sorin, to understand MAC Address use with FCoE, it&#39;s easiest to keep in mind that FCoE is really just FC operating at the L3 Network layer and using Ethernet at L2.  This means that a connection between a server and a storage that crosses two N5ks connected by VE_Ports actually consists of 3 L2 links; one between the Server and the first N5k, the second between the two N5ks and the final one between the N5k and the storage.  As with other protocols (e.g., IP) that use Ethernet as a transport, the L2 Addresses (MACs) only have meaning on each L2 link.  As a result, the are stripped off by the L3 entities (e.g., FCoE FCF, IP Routers) and new ones are used to transport the L3 protocol to the next L3 entity.  All of this means that between the Server and the first N5k, you&#39;ll use the Server&#39;s FPMA and first FCFs FCF-MAC.  Between the two N5Ks, you&#39;ll use FCF-MACs.  And between the N5k and the storage you&#39;ll use another FCF-MAC and the Storage ports FPMA.  I hope this helps! </p>
---

<p>In the April EMC Support Matrix, EMC will be posting support for NX-OS 5.0(2)N2(1) for the Nexus 5010, 5020 and 5548.&#0160; In addition, we will also now support the creation of Virtual E_Ports (VE_Ports) on these products.&#0160; This post discusses what VE_Ports are, the protocol used to instantiate them and the exact configuration steps required to create them.</p>
<p><strong><span style="text-decoration: underline;">VE_Port overview&#0160;</span></strong></p>
<p>VE_Ports allow for the formation of FCoE ISLs and the creation of an all FCoE fabric or more precisely a Multihop FCoE fabric.&#0160; As you will see, once a link between two FCFs has been established using FIP, VE_Ports / FCoE ISLs are initialized using the same protocol that is used to initialize E_Ports / native FC ISLs.&#0160; Just in case you are interested, the FIP protocol used to establish FCF to FCF connections is described in my previous post, “<a href="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/">FIP, FIP Snooping Bridges, and FCFs (Part 1 – “FIP”, the FCoE Initialization Protocol)</a>”.&#0160;</p>
<p>From a logical connectivity point of view, an all FCoE fabric is identical to an FC Fabric and it supports all of the same functionality such as zoning, a distributed name server as well as support for RSCNs.&#0160; As a result, the same types of scalability limits apply to both FC and FCoE Fabrics such as the maximum number of; hops, VN_Ports and Domains.&#0160; The FC scalability limits have been posted in the EMC Support Matrix for years and are currently no more than 5 hops, no more than 6000 N_Ports and no more than 55 Domains.&#0160; With an all FCoE fabric, I feel comfortable with 3 hops (because I’ve tested it), and have no reason to believe that the number of VN_Ports or Domains will need to be limited to less than what is supported in native FC.</p>
<p>From a physical connectivity point of view, the connectivity options currently supported for an all FCoE Fabric are shown in the following diagram.&#0160; Each of the connectivity options are explained in detail below the diagram.</p>
<p><a href="/brasstacks/fcoe-multihop-and-ve_ports/6a013487ed263f970c0147e381a0d4970b.jpg" style="display: inline;"><img alt="Figure1" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0147e381a0d4970b image-full" src="/brasstacks/fcoe-multihop-and-ve_ports/6a013487ed263f970c0147e381a0d4970b.jpg" title="Figure1" /></a>&#0160;&#0160;</p>
<p>For the sake of clarity, the diagram shows the physical connectivity options that can be used within a row of equipment racks.&#0160; The diagram is not intended to indicate a limitation in the types of topologies that are supported; rather it is just intended to help highlight all of the different possibilities.&#0160; Each Rack is described in detail below:&#0160;</p>
<p><strong>End of Row</strong>– The End of Row (EoR) cabinet contains the aggregation layer switches.&#0160; In order to maintain the highly available characteristics of FC, two 5548s are shown and they have not been connected together via FCoE ISLs.&#0160; This allows for the two fabrics to remain logically isolated.&#0160; The 5548s may be part of the same VPC Domain.&#0160;</p>
<p>The 5548s in the End of Row cabinet will support:</p>
<ol>
<li>VE_Port (FCoE ISL) connections from other Nexus 5000s, </li>
<li>VF_Port (ENode) connections from FCoE initiators and targets,</li>
<li>native FC E_Ports (ISLs) to other FC capable Cisco switches</li>
<li>F_Port (FC initiator and target) connections from FC initiators and targets.</li>
<li>N_Port connections to FC capable Cisco/Brocade/QLogic FC switches</li>
<li>uplinks from an FSB, and </li>
<li>Fabric Ports to connect to the 2232 FEX module.&#0160; </li>
</ol>
<p><strong>Rack 7 &amp; 8 Storage</strong>– Storage ports (either FC or FCoE) can be connected to a Top of Rack (ToR) switch or directly back to the 5548 in the End of Row rack (EoR).&#0160; Connecting a storage port directly to the top of rack switch in a given rack makes sense if the storage port is accessed primarily by servers residing in that rack.&#0160; If a storage port is going to be accessed by many servers in different racks, the optimal placement of the storage ports may be on the 5548 in the EoR rack.&#0160;</p>
<p><strong>Rack 5 &amp; 6 FIP Snooping Bridge (FSB)</strong>– FIP Snooping Bridges such as the Cisco/IBM 4001i can either be connected to the Nexus 5000 at the top of the rack or connected to the Nexus 5548 at the EoR.&#0160;</p>
<p><strong>Rack 4 Nexus 5000 (VE_Ports)</strong>– The Nexus 5000 can be connected to the 5548 in the EoR via VE_Ports while running in FC-SW mode over FCoE or over FC while running NPV and FC-SW modes.&#0160; Currently you cannot utilize FCoE for uplinks to the 5548 at the EoR while running in NPV mode.</p>
<p><strong>Rack 2 &amp; 3 Nexus 5000 (VE_Ports)/Nexus 2232 (Fabric Ports)</strong>– The Nexus 2232 can be connected to a Nexus 5000 via Fabric ports and then the Nexus 5000 can be connected to the Nexus 5548 at the EoR via E_Ports.&#0160;</p>
<p><strong>Rack 1 Nexus 2232 (Fabric ports) </strong>- The Nexus 2232 at the ToR can be connected to the Nexus 5548 at the EoR via Fabric ports.&#0160;</p>
<p>A logical representation of the physical topology is shown below.&#0160;</p>
<p><a href="/brasstacks/fcoe-multihop-and-ve_ports/6a013487ed263f970c014e8701c0e8970d.jpg" style="display: inline;"><img alt="Figure2" border="0" class="asset  asset-image at-xid-6a013487ed263f970c014e8701c0e8970d image-full" src="/brasstacks/fcoe-multihop-and-ve_ports/6a013487ed263f970c014e8701c0e8970d.jpg" title="Figure2" /></a>&#0160;&#0160;</p>
<p>Although it isn’t shown in the logical topology above, the FCoE ISLs must be on physically separate links rather than trunked on the ethernet uplinks used to carry non-FCoE traffic.&#0160; This is not a requirement from an FCoE protocol perspective but it is required when using the current version of NX-OS.&#0160; This requirement may eventually be removed.&#0160;</p>
<p>An important point to note in the above diagram is that from an FC logical point of view, a Fabric A / Fabric B topology has been maintained.&#0160; If the Customer desires, the ToR switches could be connected together to allow for the use of vPC and active/active NIC Teaming /Bonding.&#0160; Although this breaks the “Air gap” separation requirement (more on this later), the FC portion of the network will remain logically isolated.&#0160;</p>
<p><strong><span style="text-decoration: underline;">FCoE VE_Port Virtual Link Instantiation</span></strong></p>
<p>Note: This section describes the FCoE VE_Port Virtual Link Instantiation process currently being used between Cisco Nexus products.&#0160; The reason for this is that Cisco is the only FCF vendor currently providing this functionality.&#0160; When other vendors provide VE_Port functionality, this section will be updated to show the differences (if any).</p>
<p>The Virtual Links used to support the instantiation of Virtual E_Ports (VE_Ports) are created in a manner that is similar to the process used to instantiate a virtual link that supports the instantiation of a Virtual F_Port (VF_Port) as described in my previous post &#0160;“<a href="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/">FIP, FIP Snooping Bridges, and FCFs (Part 1 – “FIP”, the FCoE Initialization Protocol)</a>”. One major difference is that FIP VLAN Discovery is not used.&#0160; For the sake of this example, the following topology will be used.</p>
<p><a href="/brasstacks/fcoe-multihop-and-ve_ports/6a013487ed263f970c014e8701c219970d.jpg" style="display: inline;"><img alt="Figure3" border="0" class="asset  asset-image at-xid-6a013487ed263f970c014e8701c219970d image-full" src="/brasstacks/fcoe-multihop-and-ve_ports/6a013487ed263f970c014e8701c219970d.jpg" title="Figure3" /></a>&#0160;<br />&#0160;</p>
<p><strong>FIP Discovery Solicitation</strong></p>
<p>The process starts with both sides of the link transmitting DCBX frames.&#0160; Once the DCBX parameters have been exchanged, both sides will transmit Solicitations on every VLAN that FCoE has been allowed on.&#0160; In this example, we will assume that the Ethernet / vFC interface on the Nexus has been configured to allow all VLANs / VSANs.&#0160; In the diagram below, only the details for the Solicitation frames for VLAN/VSAN 100 are shown.&#0160; The Solicitations for VLAN/VSAN 200 and 300 would contain similar information.</p>
<p><a href="/brasstacks/fcoe-multihop-and-ve_ports/6a013487ed263f970c0147e381a2d6970b.jpg" style="display: inline;"><img alt="Figure4" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0147e381a2d6970b image-full" src="/brasstacks/fcoe-multihop-and-ve_ports/6a013487ed263f970c0147e381a2d6970b.jpg" title="Figure4" /></a>&#0160;&#0160;</p>
<p>The Solicitations are transmitted to the multicast Destination Address (DA) of ALL-FCF-MACs.&#0160; The SA of these frames is the Chassis MAC of the Nexus.&#0160; The 802.1Q tag will&#0160;contain the VLAN that the Solicitation is being performed on.</p>
<p>The Available for ELP bit will need to be set to one in order for FIP to proceed to the next phase (FIP Advertisement).</p>
<p>The FCF bit indicates that the Frame was transmitted by an FCF.&#0160;</p>
<p>The FC-MAP is checked by both sides to ensure that this value matches.&#0160; If it does not, FIP will not proceed to the next phase and the virtual link will not be instantiated.&#0160; The FC-MAP value prevents unintentional FC Fabric merges and should be administratively set to a value other than the default if you have multiple FCoE Fabrics in the same data center and you do not want an accidental connection between two FCFs to result in a fabric merge.&#0160;</p>
<p>The Max FCoE Size field is set to the maximum size FCoE Frame supported by each side.</p>
<p><strong>FCoE Discovery Advertisement</strong></p>
<p>If the Available for ELP bit and FC-MAP values match on both sides of the link, the FIP process will continue with both sides transmitting a Discovery Advertisement.&#0160;</p>
<p><a href="/brasstacks/fcoe-multihop-and-ve_ports/6a013487ed263f970c014e8701c368970d.jpg" style="display: inline;"><img alt="Figure5" border="0" class="asset  asset-image at-xid-6a013487ed263f970c014e8701c368970d image-full" src="/brasstacks/fcoe-multihop-and-ve_ports/6a013487ed263f970c014e8701c368970d.jpg" title="Figure5" /></a>&#0160;<br />The information contained within the FIP Discovery Advertisement is similar to what is contained in the Solicitation.&#0160; One difference worth mentioning is that the Advertisement is padded so that the Frame is equal to Max FCoE size.&#0160; The presence of this padding allows both ends to validate that the network infrastructure between the two VE_Ports is capable of supporting mini Jumbo frames.</p>
<p>Once both sides have received and validated the information contained within the Advertisements, the Virtual link can be instantiated by both sides transmitting ELP on each VLAN/VSAN that supports FCoE.&#0160; The frames exchanged to complete the VE_Port instantiation are practically identical to those frames used to initialize an FC E_Port and will not be repeated here.&#0160; For more information, refer to the <a href="http://www.emc.com/collateral/hardware/technical-documentation/h4331-networked-storage-cncpts-prtcls-sol-gde.pdf" target="_self">Networked Storage Concepts and Protocols TechBook</a> for additional information.&#0160;&#0160;&#0160;</p>
<p><strong><span style="text-decoration: underline;">Configuring Cisco VE_Ports</span></strong></p>
<p>VE_Ports allow for two Cisco Nexus 5000 products to be connected together and merged into the same fabric using FCoE links.&#0160; VE_Ports can be created as either individual links or as shown in the following example configured to use a Port channel.&#0160; The topology used in this example is shown below.&#0160;</p>
<p><a href="/brasstacks/fcoe-multihop-and-ve_ports/6a013487ed263f970c014e6026ec65970c.jpg" style="display: inline;"><img alt="Figure6" border="0" class="asset  asset-image at-xid-6a013487ed263f970c014e6026ec65970c image-full" src="/brasstacks/fcoe-multihop-and-ve_ports/6a013487ed263f970c014e6026ec65970c.jpg" title="Figure6" /></a>&#0160;</p>
<p><strong>Setup steps:</strong></p>
<p><strong>On Nexus 5000 A:</strong></p>
<p>1.&#0160; Create the appropriate VSANs</p>
<p style="padding-left: 30px;">NEXUS5000A# <strong>config t</strong></p>
<p style="padding-left: 30px;">Enter configuration commands, one per line.&#0160; End with CNTL/Z.</p>
<p style="padding-left: 30px;">NEXUS5000A(config)# <strong>vsan database</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-vsan-db)# <strong>vsan 200</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-vsan-db)# <strong>vsan 300</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-vsan-db)# <strong>vsan 400</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-vsan-db)# <strong>exit</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config)#</p>
<p>2.&#0160; Create the appropriate VLANs and associate them with the appropriate VSAN.</p>
<p style="padding-left: 30px;">NEXUS5000A(config)# <strong>vlan 200</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-vlan)#<strong> fcoe vsan 200</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-vlan)# <strong>vlan 300</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-vlan)# <strong>fcoe vsan 300</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-vlan)# <strong>vlan 400</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-vlan)#<strong> fcoe vsan 400</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-vlan)# <strong>exit</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config)#</p>
<p>3.&#0160; Create the port-channel that will be used to connect the two switches.</p>
<p style="padding-left: 30px;">NEXUS5000A(config)# <strong>interface port-channel 777</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-if)#<strong>switchport mode trunk</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-if)# <strong>exit</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config)#</p>
<p>4.&#0160; Create the vfc interface that will be associated with the port-channel, specify it as an E_Port and allow the appropriate VSANs.</p>
<p style="padding-left: 30px;">NEXUS5000A(config)# <strong>interface vfc777</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-if)# <strong>bind interface port-channel777</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-if)# <strong>switchport mode E</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-if)# <strong>no shutdown</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-if)# <strong>exit</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config)#</p>
<p>5.&#0160; Add the ethernet interfaces to the port-channel</p>
<p style="padding-left: 30px;">NEXUS5000A(config-if)# <strong>int e1/1-2</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-if-range)# <strong>switchport mode trunk</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-if-range)# <strong>channel-group 777 mode active</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config-if-range)# <strong>exit</strong></p>
<p style="padding-left: 30px;">NEXUS5000A(config)#</p>
<p>6.&#0160; Repeat steps 1 – 5 on Nexus 5000 B.</p>
<p>7.&#0160; At this point the VE_Port port-channel should initialize and can be viewed using the <strong>show fcoe database</strong> command.</p>
<p style="padding-left: 30px;">NEXUS5000A(config)# <strong>show fcoe database</strong></p>
<p style="padding-left: 30px;">-------------------------------------------------------------------------------</p>
<p style="padding-left: 30px;">INTERFACE&#0160;&#0160;&#0160;&#0160;&#0160;&#0160; FCID&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160; PORT NAME&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160; MAC ADDRESS</p>
<p style="padding-left: 30px;">-------------------------------------------------------------------------------</p>
<p style="padding-left: 30px;">…</p>
<p style="padding-left: 30px;">VE Ports:</p>
<p style="padding-left: 30px;">-------------------------------------------------------------------------------</p>
<p style="padding-left: 30px;">INTERFACE&#0160;&#0160;&#0160;&#0160;&#0160;&#0160; MAC ADDRESS&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160; VSAN</p>
<p style="padding-left: 30px;">-------------------------------------------------------------------------------</p>
<p style="padding-left: 30px;">vfc777&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;00:05:73:af:13:68&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160; 200</p>
<p style="padding-left: 30px;">vfc777&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160; 00:05:73:af:13:68&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160; 300</p>
<p style="padding-left: 30px;">vfc777&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160; 00:05:73:af:13:68&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160; 400</p>
<p style="padding-left: 30px;">NEXUS5000A(config)#</p>
<p><strong><span style="text-decoration: underline;">Afterword</span></strong></p>
<p>Last Sunday, while I was in the process of writing the technical content of this post, a friend of mine from Cisco sent me an asynchronous notification that J Metz had just posted a blog regarding <a href="http://blogs.cisco.com/datacenter/to-tell-the-truth-multihop-fcoe" target="_self">FCoE Multihop</a>.&#0160; My initial response was “Darn!” (or some variant thereof), followed by “he beat me to it!”&#0160; Well, here we are a week later and I’m finally getting around to posting my FCoE multihop post.&#0160; For the sake of transparency, let me state that because I&#0160;wanted to avoid contaminating&#0160;my thought process, this morning was the first time I actually read through the entirety of J’s post and the comments that follow.&#0160; For the most part, I found myself agreeing with J and Brad, but I understand where Brook is coming from and I think he raises some valid points that need to be seriously considered.&#0160; One point that I want to stress is this, we don’t care which protocol or topology you use to connect to our storage!&#0160; We care very much that whatever protocol or topology you do use, you are able to design, implement and maintain it with as little effort (or drama) as possible.&#0160; As long as this&#0160;is possible&#0160;we will strive to support&#0160;whatever&#0160;protocols&#0160;and topology our customers are asking for...</p>
<p>Thanks for reading!</p>
