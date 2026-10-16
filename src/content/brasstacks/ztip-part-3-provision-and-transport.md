---
title: "ZTIP – Part 3: Provision and Transport"
pubDate: 2017-12-04
postedAt: "10:09 AM"
description: "This is part 3 of a multi-part series that describes a “side-project” a small team of us (Jean Pierre (JP), Alan Rajapa and Massarrah Tannous and I) have been working on for the past couple of years. In part 1, I introduced an early version of this concept referred to..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2017/12/ztip-part-3-provision-and-transport.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250910170926/https://brasstacksblog.typepad.com/brass-tacks/2017/12/ztip-part-3-provision-and-transport.html"
pdf: "/brasstacks/ztip-part-3-provision-and-transport/ztip-part-3-provision-and-transport.pdf"
comments: []
---

<p>This is part 3 of a multi-part series that describes a “side-project” a small team of us (Jean Pierre (JP), Alan Rajapa and Massarrah Tannous and I) have been working on for the past couple of years.&#0160;</p>
<p>In <a href="/brasstacks/the-iaas-missing-link/">part 1</a>, I introduced an early version of this concept referred to as “Zero Touch <strong>Storage</strong> Provisioning” and described how it could be used to automate storage provisioning in with OpenStack.</p>
<p>In <a href="/brasstacks/zero-touch-infrastructure-provisioning-ztip/">part 2</a>, I described why we changed the name to “Zero Touch <strong>Infrastructure</strong> Provisioning” (ZTIP), provided a <a href="https://www.youtube.com/watch?v=ToANMw-sVJc&amp;feature=youtu.be">link to a video</a> that provides context about the project, introduced the IaaS overlay and underlay concepts, and then started to describe the details behind the IaaS underlay.</p>
<p>In this post I’ll continue my explanation of the IaaS underlay by starting with the Bootstrap (Provision) layer and working my way up from there.&#0160;</p>
<p><a class="asset-img-link" href="/brasstacks/ztip-part-3-provision-and-transport/6a013487ed263f970c01bb09dcf284970d.jpg" style="display: inline;"><img alt="One" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb09dcf284970d image-full img-responsive" src="/brasstacks/ztip-part-3-provision-and-transport/6a013487ed263f970c01bb09dcf284970d.jpg" title="One" /></a></p>
<h2>Bootstrap (Provision)</h2>
<p>In the last step of the previous blog post we provided a basic configuration for the network and then inventoried the servers using RackHD.&#0160; The result of this discovery process was the realization that we have three cabinets each containing a different node (compute) type (i.e., GPU capable, Storage heavy and Compute heavy).&#0160; See the diagram below.&#0160;</p>
<p><a class="asset-img-link" href="/brasstacks/ztip-part-3-provision-and-transport/6a013487ed263f970c01b8d2c42dd8970c.jpg" style="display: inline;"><img alt="Two" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b8d2c42dd8970c image-full img-responsive" src="/brasstacks/ztip-part-3-provision-and-transport/6a013487ed263f970c01b8d2c42dd8970c.jpg" title="Two" /></a></p>
<p>Since we now know the Node type, we could:</p>
<ol>
<li>Leave the nodes powered off and only power them up / load the OS when capacity needs require it. In this case only the iDRAC (BMC) interface would have an IP Address associated with it.</li>
<li>Load a default OS associated with that node type. In this case we would also want to assign the management IP to the management interface on the node once the OS is loaded.</li>
<li>Wait for the end user or a higher level orchestration layer to provide direction.</li>
</ol>
<p>In this case we’re going to assume an end user would like to configure a subset of the above nodes and we’ll refer to that subset as a Logical System.&#0160; More on this shortly.</p>
<p>An aside: I used to refer to the concept of a Logical System as a “Hardware Pool”, but switched to the term Logical System after watching the <a href="https://www.youtube.com/watch?v=RVV45YqWSzE">VxRack Manager prototype video</a>.&#0160; I’m not exactly sure what happened to VxRack Manager, but I do think they were digging in the right area. Perhaps the <a href="http://virtualgeek.typepad.com/virtual_geek/2017/04/index.html">Symphony project</a> will eventually support this kind of functionality.</p>
<p>I should also mention that I see a Logical System as being a fairly low level way to support multi-tenancy.&#0160; In other words, one or more Logical Systems could be allocated to a particular tenant for isolation purposes.&#0160;&#0160;&#0160; &#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;</p>
<h2>Transport Configuration (e.g., Ethernet + IP)</h2>
<h3>Network configuration (Phase 2): Network Slice Creation</h3>
<h4>Logical System overview</h4>
<p>For the sake of this example, we will assume that the end user has decided to create a Logical System that will require RDMA over Converged Ethernet (RoCE) to support &quot;training&quot; for the creation of a model to support real-time data analytics.&#0160; We will also assume that the user has specified the size and location of a data set that they would like to work with and that based on the size of the data set and the operation to be performed on it, someone or something (e.g., the user or some intelligent workload placement algorithm) decides that it will require 4 GPUs, 100 TB of storage capacity and 2 dense compute nodes.&#0160; We will also need connectivity to the data set (to be ingested) as well as to the Customers LAN.&#0160; Assuming each GPU capable node has 2 GPUs and each storage dense node has 25 TB of storage capacity, this could result in the following nodes being selected and included into a GPUaaS Logical System.</p>
<p><a class="asset-img-link" href="/brasstacks/ztip-part-3-provision-and-transport/6a013487ed263f970c01bb09dcf2ba970d.jpg" style="display: inline;"><img alt="Three" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb09dcf2ba970d image-full img-responsive" src="/brasstacks/ztip-part-3-provision-and-transport/6a013487ed263f970c01bb09dcf2ba970d.jpg" title="Three" /></a></p>
<p>From a network connectivity point of view, we need several different types of networks to support the connectivity and isolation requirements of this GPUaaS Logical System.</p>
<ul>
<li>Console
<ul>
<li><strong>Provides:</strong> Access to Compute Console (iDRAC)</li>
<li><strong>Instantiation:</strong> Tenant (i.e., Logical System) specific Management LAN on Management Network</li>
<li><strong>Note:</strong> Once a compute resource has been dedicated to a particular logical system, its BMC interface will need to be isolated from all other system resources that do not belong to the same Logical System. This could be accomplished via ACLs on the management plane switches (e.g., Dell N3000 series)</li>
</ul>
</li>
<li>Management
<ul>
<li><strong>Provides:</strong> Access to the physical management interface on Compute instances.</li>
<li><strong>Instantiation:</strong> Tenant (i.e., Logical System) specific Management LAN on Management Network could be the same network as the Console network as long as these interfaces do not need to be remotely accessible.</li>
</ul>
</li>
<li>LAN:
<ul>
<li><strong>Provides:</strong> VM / Container to world connectivity.</li>
<li><strong>Instantiation:</strong> Tenant specific LAN Overlay Virtual Network on the “Default slice” of the Data Network. (Note: more information about the concept of a slice will be provided below)</li>
</ul>
</li>
<li>ScaleIO 1:
<ul>
<li><strong>Provides:</strong> Dedicated/Isolated connectivity between compute nodes for ScaleIO traffic.</li>
<li><strong>Instantiation:</strong> A “ScaleIO 1” network slice on Data Network with each interface ideally being allocated a minimum bandwidth.</li>
</ul>
</li>
<li>ScaleIO 2:
<ul>
<li><strong>Provides:</strong> Dedicated/Isolated connectivity between compute nodes for ScaleIO traffic.</li>
<li><strong>Instantiation:</strong> A “ScaleIO 2” network slice on Data Network with each interface ideally being allocated a minimum bandwidth.</li>
</ul>
</li>
<li>Ingest:
<ul>
<li><strong>Provides:</strong> Connectivity to the location of the data source.</li>
<li><strong>Instantiation:</strong> A “Data Ingest” network slice on Data Network with each interface allocated a minimum bandwidth.</li>
</ul>
</li>
<li>GPU:
<ul>
<li><strong>Provides:</strong> RDMA connectivity between the GPU and the Storage nodes.</li>
<li><strong>Instantiation:</strong> A “RoCE” network slice on Data Network with each interface allocated a minimum bandwidth and the network itself configured to support RoCE (i.e., PFC and ECN).</li>
</ul>
</li>
</ul>
<h3>Network Slices</h3>
<p>Some of the networks described above are instantiated as network “slices”.&#0160; Before we dig into the reason for this, let’s start with a definition.</p>
<p><em>A network &quot;slice&quot; is an Underlay Virtual Network that has been instantiated for the purposes of logically isolating a portion of a physical network topology.&#0160; Each slice can have specific attributes assigned to it (e.g., DCB) which, for example, would allow for the transport of a protocol that requires losslessness (e.g., RoCE).&#0160; A slice typically consists of at least two VLANs connected via an L3 (routed) portion of the network.&#0160; The characteristics of a slice (e.g., losslessness) are expected to span the Network Topology from ingress to egress.</em></p>
<p>A slice is different from an Overlay Virtual Network (e.g., VXLAN) because slices are instantiated on, and require special handling from, network hardware to support the requirements of the traffic that will be transported (e.g., RoCE).&#0160; Because each traffic class can consume finite network hardware resources (e.g., HW queues), we believe that it would be necessary to reuse slices across different tenants but in order to maintain tenant isolation, it will probably require the use of something like an Overlay Virtual Network (e.g., VXLAN).</p>
<p>A final note on the concept of a slice.&#0160; I think it’s fair to say that this concept was, at the very least, inspired by the work that a group of folks at Jeda Networks did with FCoE a few years back.&#0160; The key difference is their approach was used to support FCoE traffic and we’re thinking of using the concept in a more general purpose kind of way.&#0160;</p>
<p>Just to highlight the difference between the underlay (e.g., a slice) and the overlay (e.g., an Overlay Virtual Network), I’ll provide an example from some related work (below). &#0160;&#0160;Please note, although the following diagram provides an illustration of the slices concept using iSCSI over RoCE, the same principles could eventually be applied to other protocols such as NVMe over RoCE.</p>
<p><a class="asset-img-link" href="/brasstacks/ztip-part-3-provision-and-transport/6a013487ed263f970c01b7c939d4fe970b.jpg" style="display: inline;"><img alt="Four" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b7c939d4fe970b image-full img-responsive" src="/brasstacks/ztip-part-3-provision-and-transport/6a013487ed263f970c01b7c939d4fe970b.jpg" title="Four" /></a></p>
<p>In order to allow multiple tenants (e.g., Red, Green and Blue) to share each slice would probably require the use of an Overlay Virtual Network.&#0160; These Overlay Virtual Networks are shown below as colored lines and could be configured at any point after the Slices have been created.&#0160;</p>
<p><a class="asset-img-link" href="/brasstacks/ztip-part-3-provision-and-transport/6a013487ed263f970c01bb09dcf2cf970d.jpg" style="display: inline;"><img alt="Five" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb09dcf2cf970d image-full img-responsive" src="/brasstacks/ztip-part-3-provision-and-transport/6a013487ed263f970c01bb09dcf2cf970d.jpg" title="Five" /></a></p>
<p>An example of how this concept might be applied to a physical network is provided below.</p>
<p><a class="asset-img-link" href="/brasstacks/ztip-part-3-provision-and-transport/6a013487ed263f970c01b7c939d513970b.jpg" style="display: inline;"><img alt="Six" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b7c939d513970b image-full img-responsive" src="/brasstacks/ztip-part-3-provision-and-transport/6a013487ed263f970c01b7c939d513970b.jpg" title="Six" /></a></p>
<p>As shown above the storage slice connects the Compute nodes containing GPUs in Rack A to the Storage dense nodes in Rack B.&#0160; This slice will ensure that there’s at least 3 Gbps of bandwidth available per interface (oversubscription could impact this) and also ensure that the links that transport the traffic support PFC and ECN.</p>
<p>There is so much additional detail I could provide about the slices + OVN concept shown above.&#0160; Areas of interest for me have been things like how to address the complexity associated with applying a BW limit at the slice layer and then further subdividing this BW at the OVN layer.&#0160; It’s an area that’s ready for some serious innovation but again, you could probably find a networking vendor who could simplify this problem for you.</p>
<p>If you’d like to see some related work that we’ve previously done in this space, see the “<a href="/brasstacks/an-introduction-to-virtual-storage-networks/">An Introduction to Virtual Storage Networks</a>” blog post series.</p>
<p>Today, there are many different approaches that could be used to instantiate a slice, but in this case we will assume that something like the steps described by Mellanox in “<a href="https://community.mellanox.com/docs/DOC-2591">How To Configure Mellanox Spectrum Switch for Lossless RoCE</a>” have been performed.</p>
<h3>Compute Node Physical Interface Configuration&#0160;</h3>
<p>To allow a compute node to access a specific slice, you would need to configure the switch interface to allow access to the VLAN associated with the slice and then configure the compute node interface to access the appropriate VLAN.&#0160; A couple of points about this:</p>
<ol>
<li>I am assuming that the network will be configured with the L3 boundary at the ToR (Leaf) switch and this may not always be the case.</li>
<li>In order to know what switch interfaces you’ll to configure, you will need to know where each server interface (that is part of this logical system) is attached and what each interface will be used for. This is one of those causality dilemma’s I described earlier and would be solved by a topology service.&#0160;</li>
</ol>
<h2>Service (e.g., ScaleIO) configuration</h2>
<p>Once the Transport layer (e.g., slice) has been configured and you have optionally configured OVN, you can start deploying and configuring the services that will use them.&#0160; One example would be ScaleIO and we described how you could do this in the <a href="https://www.youtube.com/watch?v=ToANMw-sVJc">ZTIP demo</a>.&#0160; Apparently, based on the <a href="http://virtualgeek.typepad.com/virtual_geek/2017/05/dell-emc-world-2017-scaleio-30.html">information that has already been made publicly available</a>, you will also soon be able to use AMS to perform the same steps.&#0160;</p>
<p>In the next blog post I’ll provide another example that uses iSCSI and perhaps an NVMe over RoCE example after that. :-)&#0160;</p>
<p>Thanks for reading!</p>
