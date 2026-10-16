---
title: "Zero Touch Infrastructure Provisioning (ZTIP)"
pubDate: 2017-12-01
postedAt: "11:04 AM"
description: "This is part 2 of a multi-part series that describes a “side-project” a small team of us (Jean Pierre (JP), Alan Rajapa and Massarrah Tannous and I) have been working on for the past couple of years. You’ll note that in part 1 of the series, I was referring to..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2017/12/zero-touch-infrastructure-provisioning-ztip.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250911101045/https://brasstacksblog.typepad.com/brass-tacks/2017/12/zero-touch-infrastructure-provisioning-ztip.html"
pdf: "/brasstacks/zero-touch-infrastructure-provisioning-ztip/zero-touch-infrastructure-provisioning-ztip.pdf"
comments: []
---

<p>This is part 2 of a multi-part series that describes a “side-project” a small team of us (Jean Pierre (JP), Alan Rajapa and Massarrah Tannous and I) have been working on for the past couple of years.&#0160;</p>
<p>You’ll note that in <a href="/brasstacks/the-iaas-missing-link/">part 1</a> of the series, I was referring to a similar concept as “Zero Touch <strong>Storage</strong> Provisioning”.&#0160; The reason for the name change was that along the way, we figured out that we were trying to provision WAAAY more than just storage, so we changed the name to “Zero Touch <strong>Infrastructure</strong> Provisioning” (ZTIP).&#0160;</p>
<p>Before we begin, if you’d like to get an idea of the overall concept, as well as see a snapshot of where we were in the journey about 18 months ago, please see <a href="https://youtu.be/ToANMw-sVJc">this video</a> that was put together by Massarrah and JP.&#0160; We (ok, I) like quirky names, so please do not hold the name of our controller “Orchestration System for Infrastructure Management” (OSIM) against <strong><u>them</u></strong>. :-)</p>
<h1>Underlays and overlays&#0160;</h1>
<p>Our work rests on the idea that Infrastructure as a Service (IaaS) can be logically broken down into at least 2 layers; the IaaS overlay and the IaaS underlay.</p>
<p><a class="asset-img-link" href="/brasstacks/zero-touch-infrastructure-provisioning-ztip/6a013487ed263f970c01b8d2c36148970c.jpg" style="display: inline;"><img alt="One" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b8d2c36148970c image-full img-responsive" src="/brasstacks/zero-touch-infrastructure-provisioning-ztip/6a013487ed263f970c01b8d2c36148970c.jpg" title="One" /></a></p>
<h2>The IaaS Overlay</h2>
<p>Most of you are probably very familiar with the IaaS Overlay and the IaaS Overlay Management and Orchestration (M&amp;O) software used to control it.&#0160; A couple of examples would be VMware vRealize Automation, OpenStack and whatever Amazon is using to orchestrate Amazon Web Services (AWS) more specifically EC2.&#0160;</p>
<p>Based on the work we’ve done and the research we’ve seen performed by others in the industry, I believe the IaaS Overlay is all about the well-known axiom “Abstract, Pool, Automate”.&#0160; Judging by the solutions I see available for use in the Enterprise, I think many others would say the same.&#0160; &#0160;</p>
<h2>The IaaS Underlay</h2>
<p>Most of you are probably not as familiar with the IaaS Underlay and the IaaS Underlay M&amp;O software used to control it.&#0160;&#0160; I would LOVE to provide examples, but we’ve been working in this space because we haven’t found a solution (suitable for on-premises use in the Enterprise) that does everything we need.&#0160; And by everything, I mean everything in the red (dashed) box shown below.</p>
<p><a class="asset-img-link" href="/brasstacks/zero-touch-infrastructure-provisioning-ztip/6a013487ed263f970c01b8d2c3614d970c.jpg" style="display: inline;"><img alt="Two" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b8d2c3614d970c image-full img-responsive" src="/brasstacks/zero-touch-infrastructure-provisioning-ztip/6a013487ed263f970c01b8d2c3614d970c.jpg" title="Two" /></a></p>
<h1>The IaaS Underlay explained</h1>
<p>The diagram above can be broken down into:</p>
<ul>
<li>Columns that represent resources (e.g., Compute and Network) or actors (e.g., people or services that perform a particular function); and</li>
<li>Rows that represent logical layers of the infrastructure as well as the configuration steps that are common to the resources in each column.</li>
</ul>
<p><em>An aside: You might ask “what happened to the “Storage” column you were showing in <a href="/brasstacks/the-iaas-missing-link/">the previous blog post</a>?” and that’s a phenomenally interesting story that will have to wait for my “post-retirement” book.&#0160; That said, the removal of the storage column is one reason for the name change to ZTIP.&#0160; The other primary reason is; we’ve been focusing on Hyper-converged solutions for full stack automation.&#0160; This is because the concept of automation is something that traditional enterprises still seem to be evaluating, whereas the HCI community seems to have embraced it fully.&#0160; </em></p>
<p>For the remainder of this blog series, I’ll explain each of the layers (rows) in the above diagram and I’ll start from the bottom and work my way to the top.&#0160;</p>
<p>Before I continue, I’d like to share an observation that was made during the course of our work.&#0160; Essentially, we noticed that the lower we went in the stack, the harder it was to automate.&#0160; I’ll provide more detail about this when I get up to the mapping layer case study, but I think this is a big reason why so few people have attempted to fully automate the IaaS underlay.</p>
<h2>The Physical Layer</h2>
<p>Although everything ultimately runs on physical resources, I don’t consider the physical configuration of the components to be within the domain of the IaaS Underlay M&amp;O controller.&#0160; That said, we should at least mention that fact that before any of these components can be configured, each of them will need to be Racked, Cabled and Powered (R,C,P).&#0160; This is a process that will be performed by a person, at least until the singularity, and at that point Robots will be people too (and even they will probably be asking “isn’t there some way we can automate this?”).&#0160; &#0160;</p>
<h2>Bootstrap – Node Creation</h2>
<p>Once the nodes have been Racked, Cabled and Powered, a body of work comes into play that I’ll refer to as Composable Systems.&#0160; The basic idea is that you will eventually be able to dynamically select CPU, Memory, Storage, GPUs, etc from pools of resources and then instantiate a “virtual” bare metal server that has exactly the right requirements for your application.&#0160; It’s an area that is still in its infancy but <a href="https://blog.dellemc.com/en-us/server-disaggregation-sometimes-the-sum-of-the-parts-is-greater-than-the-whole/">this blog post by Dell’s Bill Dawkins</a> contains some great additional information.&#0160;</p>
<p>Because this area is still so new, I don’t currently include it when I talk about the IaaS underlay.&#0160; That said, once a “Server Builder” API is available, it would make sense to include it.</p>
<h2>Bootstrap – Inventory</h2>
<p>Today, the lowest layer of the IaaS Underlay is the Bootstrap Inventory layer and the first bit of configuration that will need to be done in this layer is to configure the network.&#0160;</p>
<h3>Network Configuration (Auto-config Leaf/Spine + gather LLDP)</h3>
<p>As will become clear as we move up the IaaS stack, there are all kinds of causality dilemmas (chicken or the egg scenarios) when trying to bootstrap Infrastructure and many of them can be solved by understanding how the elements you are trying to configure are related to one another, or put another way, how they are interconnected.&#0160; I refer to these interconnectivity details as “topology information” and to properly understand the topology, I believe it makes sense to use the network as the source of truth. (h/t to Nick Ciarleglio from Arista networks for this insight)</p>
<p>However, before we can understand the topology, we first need to configure the network elements that will be providing the connectivity and hence we have our first causality dilemma (e.g., how do we configure the network if we don’t know exactly what it will be used for?)&#0160; One approach that can be used is to configure the network in stages, and the first phase is something that I’ve been referring to as “IP Fabric formation”.</p>
<p>IP Fabric formation is basically just a way to say we are going to configure the switches so that they have basic connectivity between themselves. &#0160;</p>
<p>With regards to the IP Fabric formation process itself, there seem to be three primary ways to accomplish this task:</p>
<ol>
<li>Acknowledge it’s a huge pain-in-the-rear to automate basic network connectivity and just configure the network manually!</li>
<li>Use a discovery protocol to determine the physical connectivity information (i.e., how you physically connected the switches together) and then use this information to determine how to form the fabric.</li>
<li>Buy a solution that does this for you! Three solutions that provide this functionality, and that I also have at least a passing familiarity with, are: Big Switch, Plexxi and Mellanox (Neo).&#0160; &#0160;</li>
</ol>
<p>We’ve done it all three ways: &#0160;</p>
<ol>
<li>Manual or template configuration is a good approach to use if you have a standardized network topology.</li>
<li>Using topology information to <a href="/brasstacks/how-to-determine-a-switchs-role-in-a-clos-network-with-mlagd-leaves/">determine how to configure the network</a> is possible if you know something about your network’s characteristics and you have some dev resources to spare. For a bit more information about how you might accomplish this see the Network Configuration Example (below).</li>
<li>I think buying a solution rather than attempting to DIY a fabric controller makes the most sense for the vast majority of use cases. Of the Implementations that I mentioned above (i.e., Big Switch, Plexxi and Mellanox), I have the most experience with Plexxi and I PERSONALLY really like their BW limit feature.&#0160; <em>Disclosure: We’ve written a <a href="https://support.emc.com/search/?text=docu79674">white paper</a> with Plexxi on the topic of Secure iSCSI SANs and used BW limits in that paper.</em></li>
</ol>
<h3>End device discovery (ID+INV Advertise LLDP)</h3>
<p>Once the switches have a basic configuration on them and basic connectivity established between them, you can do a couple of very interesting things:</p>
<ol>
<li>Gather information about the connected end devices. We used LLDP in our <a href="/brasstacks/the-iaas-missing-link/">ZTSP PoC</a> and it seems like a really good approach to use if the end devices that you’ll be attaching to your network actually support it.</li>
<li>Once you determine where the end devices are attached (LLDP), you can ID and inventory (INV) them. We use <a href="https://github.com/RackHD">RackHD</a> in all of our PoC’s and it does everything we need it to.&#0160; Once slight caveat to keep in mind is that it currently performs the inventory by downloading a uKernel via PXE and this also requires the use of DHCP.&#0160; As a result, you’ll need to either allow for this traffic over a “default” VLAN or do some routing tricks if you’re using an L3 Leaf/Spine.&#0160; That said, we’ve also experimented with using Dell’s iDRAC interface for the purposes of performing inventory over the management network and this seems like a really interesting approach.&#0160; I should also point out there are other approaches (e.g., <a href="https://github.com/puppetlabs/Razor-Microkernel">Razor</a>) that can be used in place of RackHD.</li>
</ol>
<p>So with the above in mind, let’s look at an example that describes (at a high level) some of the work we’ve done in this space.</p>
<h2>Network Configuration Example</h2>
<p>The following configuration of Compute and Network resources will be used throughout this blog post series.</p>
<p><a class="asset-img-link" href="/brasstacks/zero-touch-infrastructure-provisioning-ztip/6a013487ed263f970c01bb09dc2a64970d.jpg" style="display: inline;"><img alt="Three" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb09dc2a64970d image-full img-responsive" src="/brasstacks/zero-touch-infrastructure-provisioning-ztip/6a013487ed263f970c01bb09dc2a64970d.jpg" title="Three" /></a></p>
<p>This configuration consists of:</p>
<ul>
<li>Three <strong>Spine switches</strong>. (i.e., MAC Addresses of AA, BB and CC)</li>
<li>Three pairs of <strong>Leaf Switches</strong> that are intended to be MLAG’d together. (i.e., MAC Addresses of DD/EE, FF/GG and HH/JJ)</li>
<li>A pair of <strong>Border Leaf switches</strong> that are intended to be MLAG’d together. (i.e., MAC Addresses of YY/ZZ)</li>
<li>Some number of Connections to the customer’s LAN</li>
<li>An L2 <strong>Management Network</strong></li>
<li>Fourteen General Purpose <strong>Compute nodes</strong>.</li>
<li>One <strong>Control Node</strong> where we will assume the <strong>Centralized Network Control Point</strong> will be running.</li>
</ul>
<h2>Overall Assumptions</h2>
<ul>
<li>The Network hardware elements to be configured (leaf and spine switches) can be managed from a “centralized network controller”. In this case, we’ll assume that we’re going to “roll our own” versus buying one.&#0160;</li>
<li>The Control Node will:
<ul>
<li>be physically connected to the management and Leaf switches that physically reside in the same cabinet as the Control Node itself.</li>
<li>provide a DHCP service</li>
</ul>
</li>
<li>Power has been supplied to all of the cabinets and switch hardware including the spine switches that are not shown as residing in a cabinet in the example configuration diagram.</li>
<li>The Control Node will power up and the Centralized Network Controller will be able to discover (e.g., via LLDP) at least the management and leaf switches that it is directly connected to.</li>
<li>The switches have obtained an IP Address from the DHCP server running on the Control Node</li>
</ul>
<h2>Phase 1: IP Fabric formation</h2>
<h3>Phase 1 assumptions</h3>
<ol>
<li>All of the switches are at their factory default settings,</li>
<li>The user has obtained at least one MAC Address of one of the Spine switches (e.g., by examining a label on one of the switches). This information is optional and will only be needed if the end user wants to verify the correct roles have been assigned to each switch type.&#0160;</li>
<li>The switches have a NOS preinstalled on them (but this may not always be the case).</li>
</ol>
<h3>Topology discovery</h3>
<ol>
<li>When the switches first boot, they should attempt to download a configuration from the centralized network controller (e.g., POAP, ZTP, ONIE+). If a switch’s role is unknown (e.g., unknown switch MAC Address), the Network Controller will associate the “Topology Discovery Configuration” with it and the switch will use this configuration until after Topology discovery has been completed and a role has been assigned to each switch (e.g., Spine, Leaf, Border Leaf).&#0160; NOTE: The switch role (e.g., Spine, Leaf, Border Leaf) could also be set at the factory.</li>
<li>Once every unknown switch is running the Topology Discovery Configuration, the LLDP information being received by each switch can be stored in a centralized topology database.
<ol>
<li>Note, we used MongoDB for this purpose in the ZTIP PoC.</li>
</ol>
</li>
<li>The network controller can use the process defined in <a href="/brasstacks/how-to-determine-a-switchs-role-in-a-clos-network-with-mlagd-leaves/">this blog post</a> to attempt to determine the role of each switch that has been discovered. The roles that have been assigned to each switch can be modified later during the IP Fabric configuration process. &#0160;</li>
</ol>
<h3>IP Fabric configuration</h3>
<ol>
<li>The user launches the Fabric configuration wizard. See the <a href="https://youtu.be/ToANMw-sVJc">ZTIP Demo</a> at timestamp 1:38 for more information.&#0160;</li>
<li>When the Fabric configuration wizard is launched, the user will be allowed to:
<ol>
<li>Set / modify the switch roles (e.g., leaf, spine) in this configuration. The wizard could obtain a list of switches and their discovered or factory preassigned roles from the centralized topology database.</li>
<li>Use or override the pre-provided pool of IP Addresses that will be used for IPv4 fabric (switch to switch) links.</li>
<li>Use or override the pre-provided pool of IP Addresses that will be used for the router IDs.</li>
<li>Use or override the pre-provided pool of IP Addresses that will be used for the creation of VLAN interfaces on the switches in the environment.</li>
</ol>
</li>
<li>Once the switch roles have been determined, the IP Fabric configuration service will use the switch role and topology information stored in the centralized topology database to create a candidate IP Fabric topology like the one shown below. Please note, the following diagram is just a simplified version of the example configuration shown above.&#0160; Also note that IPv4 Addresses have been assigned to each switch interface and a router ID has been provided to each switch as well.&#0160; We could have used IPv6 but have encountered a switch vendor specific issue that prevented us from doing so during testing. In any case, this is merely an example of what could be done, not what should be done.&#0160;&#0160;&#0160;&#0160; &#0160;&#0160;&#0160;&#0160;</li>
</ol>
<p><a class="asset-img-link" href="/brasstacks/zero-touch-infrastructure-provisioning-ztip/6a013487ed263f970c01b7c9391052970b.jpg" style="display: inline;"><img alt="Four" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b7c9391052970b image-full img-responsive" src="/brasstacks/zero-touch-infrastructure-provisioning-ztip/6a013487ed263f970c01b7c9391052970b.jpg" title="Four" /></a></p>
<ol start="4">
<li>Once the candidate IP Fabric topology has been created, the network controller can create configurations for each of the switches in the topology.</li>
<li>Configure Leaf to end device links</li>
</ol>
<p>Note: Initially all end device interfaces (e.g., eth7 and above) could be put into a default VLAN (e.g., 4001) for the purposes of PXE boot and inventory.&#0160; This will allow the hosts to obtain an IP Address, PXE boot and then perform inventory.</p>
<ol start="6">
<li>Repeat the above steps for each switch that was discovered. When finished each switch should have a configuration file associated with it.</li>
<li>The switches could now be restarted and download their configuration files from the centralized network controller or something like Ansible or Puppet could be used to set the switch configuration.</li>
</ol>
<p>At this point the IP Fabric has been formed and the compute resources should be able to PXE boot and download the RackHD microkernel to start the inventory process.&#0160; We will assume that once the inventory process has completed, the capabilities of each node are as shown below.</p>
<p><a class="asset-img-link" href="/brasstacks/zero-touch-infrastructure-provisioning-ztip/6a013487ed263f970c01b7c939105b970b.jpg" style="display: inline;"><img alt="Five" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b7c939105b970b image-full img-responsive" src="/brasstacks/zero-touch-infrastructure-provisioning-ztip/6a013487ed263f970c01b7c939105b970b.jpg" title="Five" /></a></p>
<p>Note that each rack contains homogeneous node types but this won’t typically be the case.&#0160; Also note that “GPU” indicates that the node contains GPUs, while “Storage” and “Compute” indicate that the nodes are either Storage “heavy” or Compute “heavy”.</p>
<p>The remainder of the network configuration process (e.g, Slice creation) will be handled as workloads are on-boarded and will be discussed in the next blog post.</p>
<p>Thanks for reading!</p>
