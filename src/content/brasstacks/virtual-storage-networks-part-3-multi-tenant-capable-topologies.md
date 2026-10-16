---
title: "Virtual Storage Networks – Part 3 (Multi-tenant capable topologies)"
pubDate: 2014-05-01
postedAt: "04:40 PM"
description: "This is part three of a blog series that describes a new concept we're referring to as a Virtual Storage Network. In part 1 of this series, I introduced the Virtual Storage Network or VSN as concept that enables the dynamic creation of storage service compositions. I also provided some..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2014/05/virtual-storage-networks-part-3-multi-tenant-capable-topologies.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250911153553/https://brasstacksblog.typepad.com/brass-tacks/2014/05/virtual-storage-networks-part-3-multi-tenant-capable-topologies.html"
pdf: "/brasstacks/virtual-storage-networks-part-3-multi-tenant-capable-topologies/virtual-storage-networks-part-3-multi-tenant-capable-topologies.pdf"
comments: []
---

<p>This is part three of a blog series that describes a new concept we&#39;re referring to as a&#0160;<a href="/brasstacks/an-introduction-to-virtual-storage-networks/" target="_self">Virtual Storage Network</a>. &#0160;</p>
<p>In <a href="/brasstacks/virtual-storage-networks-part-1/" target="_self">part 1</a> of this series, I introduced the Virtual Storage Network or VSN as concept that enables the dynamic creation of storage service compositions. &#0160;I also&#0160;provided some background information and stated what we believe the requirements for multi-tenant storage are. &#0160;</p>
<p>In <a href="/brasstacks/virtual-storage-networks-part-2-requirements-for-multi-tenant-storage/" target="_self">part 2</a>, I provided additional detail about the multi-tenant storage requirements and made reference to a couple of topologies that could satisfy these requirements to one degree or another.</p>
<p>In this installment, I’ll discuss these topologies and explain how many of today’s infrastructure elements are unable to support multi-tenant isolation.</p>
<p>Before I go too much further, I need to clarify a few points.&#0160;</p>
<ol>
<li>In the previous two posts, I used the term “multi-tenancy” somewhat liberally to describe an environment consisting of a single set of resources that could be utilized by some number of tenants, but I never actually defined what I meant by &quot;tenant&quot;. &#0160;For the remainder of this post, assume that a tenant consists of</li>
<ul>
<li>one or more Virtual Machines,</li>
<li>one or more Virtual Networks for LAN connectivity,</li>
<li>some amount of storage capacity, and</li>
<li>zero or more Virtual Storage Networks (VSNs) to connect the VMs to their storage capacity.</li>
</ul>
<li>Outside of the VSN concept, all of the tenant elements described above exist today. &#0160; &#0160;&#0160;</li>
<li>In the introduction above, I made the statement that many of today’s infrastructure elements are unable to support “multi-tenant <strong>isolation</strong>”.&#0160; I did not say that today&#39;s infrastructure elements are unable to support &quot;multi-tenancy&quot;. &#0160;This is a subtle yet important difference that will hopefully become a bit clearer as you read through this post.</li>
<li>Even though I believe many infrastructure elements are unable to multi-tenant isolation today, I am not, in any way, trying to imply that multi-tenant <strong>isolation</strong> is necessary or even desirable in all “multi-tenant” use cases.&#0160; For example, I’m not trying to say that in a VDI environment we should be allocating a VSN to each VDI instance!&#0160; But, it may eventually make sense to allow groups of instances (e.g., a tenant) to attach to a VSN that has been setup specifically for that group.</li>
<li>The final point is the difference between “multi-tenant” and “multi-instance”.&#0160; Multi-tenancy describes a model of resource sharing where multiple tenants are provided isolated access to a single instance of a resource.&#0160; Multi-instance describes a model where each tenant is given access to their own separate instance of a particular resource.&#0160; For more information, see <a href="https://en.wikipedia.org/wiki/Multitenancy" target="_self">Wikipedia</a>, this <a href="http://gigaom.com/2014/01/26/multi-tenant-or-multi-instance-cloud-lets-do-both/" target="_self">gigaom blog post</a>&#0160;or this <a href="http://fayebsg.com/2013/05/multi-tenancy-vs-multi-instance/" target="_self">SugarCRM post</a>.&#0160;</li>
</ol>
<h2>Satisfying Storage requirements</h2>
<p>Recall that in <a href="/brasstacks/virtual-storage-networks-part-2-requirements-for-multi-tenant-storage/" target="_self">part 2</a>, I provided a list of seven storage requirements and described why they were needed.&#0160; For your reference, I’ve provided this list below and&#0160;will explain how each topology shown meets or fails to meet these requirements.&#0160;</p>
<ol start="1" type="1">
<li>Namespace isolation</li>
<li>Prevent noisy neighbor problems</li>
<li>Provide Bandwidth /IOPS / response time guarantees</li>
<li>Tenant traffic identification</li>
<li>Storage Network Service Insertion (e.g., encryption)</li>
<li>Authentication (e.g., CHAP)</li>
<li>Do not rely on Guest OS resident iSCSI initiators</li>
</ol>
<h2>Topology 1</h2>
<p>The first topology I’ll describe is shown below and has been logically sliced into vertical layers. &#0160;From left to right these layers are compute, a front end network, a storage layer and then a back end network.&#0160; It has also been physically sliced into horizontal layers with Row 1 on the top and Row n on the bottom. &#0160;&#0160;Each row could consist of some number of hypervisors or non-virtualized servers and one or more storage array instances.&#0160; The front end and back end networks could utilize the same physical network.</p>
<p><a class="asset-img-link" href="/brasstacks/virtual-storage-networks-part-3-multi-tenant-capable-topologies/6a013487ed263f970c01a73da95133970d.jpg" style="display: inline;"><img alt="One" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01a73da95133970d image-full img-responsive" src="/brasstacks/virtual-storage-networks-part-3-multi-tenant-capable-topologies/6a013487ed263f970c01a73da95133970d.jpg" title="One" /></a></p>
<p>Note that each hypervisor is hosting multiple tenants and each tenant has associated with it:&#0160;</p>
<ul>
<li>one or more VMs;</li>
<li>LAN connections (not shown for clarity); and</li>
<li>in this case a single VVOL Protocol Endpoint (PE) essentially a SCSI Logical Unit (LU) containing multiple VVOLs.&#0160; Each VVOL PE could be presented as a LU behind a tenant specific Target inside of a VSA.</li>
</ul>
<p>For reasons that should become clear shortly and will be expanded upon in part 4 of the series; I’ve designated portions of the networks as “non-blocking regions” and have associated these regions with a Row.&#0160; This non-blocking network could use FC, Ethernet or IB as a transport and make use of any protocol supported on the transport of choice.&#0160;</p>
<p>Another point to keep in mind; although I’m showing VVOLs above, I’m not implying that only VMware could be used.&#0160; This kind of topology could be used with any kind of hypervisor.</p>
<p>The Storage arrays have been logically segmented into Virtual Storage Appliances (VSA). &#0160;For the sake of example, you could probably think of these as being similar to VNX Virtual Data Movers (VDMs). &#0160;Each VSA provides a Target (T) interface that can be accessed by an Initiator on the Hypervisor. &#0160;Since I&#39;m not trying to limit the protocols that can be supported by this model, I feel it&#39;s important to point out that you could replace the &quot;INIT&quot; function on the host with &quot;Client&quot; and the &quot;T&quot; function on the storage with &quot;Server&quot; and it will not impact the model in general. &#0160;Also note that each VSA has back end connections. &#0160;These connections would be used for replication and mobility (refer to the <a href="/brasstacks/fast-sideways-a-connectivity-point-of-view/" target="_self">FAST Sideways</a> use case for information that describes how these connections could be used). &#0160;</p>
<p>Finally, Topology 1 does not <span style="text-decoration: underline;">require</span> any changes to existing storage stacks running in today’s (existing) hypervisor or non-virtualized Operating Systems.&#0160; That having been said, the ability to identify the storage belonging to a VM is a compelling feature that needs to be accounted for in the design.&#0160; In an ESX environment, this would require the use of something like VVOLs (when available).&#0160; With other Hypervisors (e.g., KVM based) you could just deal with individual Storage Volumes (LUs) that are presented from the array.&#0160;&#0160;BTW,&#0160;there are other options for identifying the storage belonging to a particular VM but I am not going to discuss them at this point.</p>
<p><span style="font-size: 1.5em;">Satisfying storage requirements with Topology 1</span></p>
<p>In this section I&#39;ll evaluate topology 1 to determine if it meets the requirements described in <a href="/brasstacks/virtual-storage-networks-part-2-requirements-for-multi-tenant-storage/" target="_self">Part 2</a>&#0160;of this series.</p>
<h3>Namespace Isolation</h3>
<p>This requirement is partially met by Topology 1.&#0160; The particular problem I focused on in the requirement definition was related to multiple OpenStack instances attempting to utilize the same array.&#0160; Assuming that VSAs are being used and each VSA has an isolated name space, this use case could be supported by this kind of topology.&#0160; The problem is, this topology does not address the <a href="http://blog.scottlowe.org/2013/09/04/introducing-linux-network-namespaces/" target="_self">namespace</a> issue on the compute node and as you will see, this will cause problems with other requirements.</p>
<h3>Prevent noisy neighbor problems</h3>
<p>This requirement is not met by Topology 1.&#0160; There’s nothing to prevent acute network related noisy neighbor problems caused by one tenant from impacting another.&#0160; However, the problem could probably be mitigated somewhat by using a non-blocking network topology between the compute and the storage and then being careful about how heavily you load each host and array interface.&#0160; Also, chronic problems could be detected and the be resolved via a mechanism like <a href="/brasstacks/fast-sideways-a-connectivity-point-of-view/" target="_self">FAST sideways</a>.</p>
<h3>Provide Bandwidth, IOPS and Response Time guarantees</h3>
<p>This requirement is not met by Topology 1.&#0160; There’s only a single initiator per hypervisor and this means that something similar to the <a href="http://searchvirtualstorage.techtarget.com/definition/I-O-Blender" target="_self">IO blender</a> issue could still cause cross-tenant problems. &#0160;I&#39;m not saying the Bandwidth, IOPS and Response Time guarantees you can configure today won’t work, they just do not provide this functionality at the correct level of granularity (e.g., on a per tenant basis) or from an end-to-end point of view. &#0160;</p>
<h3>Tenant Traffic Identification and Storage Network Service Insertion</h3>
<p>This requirement could partially be met by Topology 1.&#0160; Although VVOLs (or alternatively one LU per VM) will allow for per VM traffic identification, there is no way to identify a particular Tenant’s storage traffic and differentiate it from another Tenant&#39;s storage traffic.&#0160; This is because even if you had a map of every VM (via LUN) to Tenant relationship, in order for you to identify and perform actions on all tenant traffic, you would need to keep an enormous amount of state information (e.g., which FC exchanges belong to which tenant) and be able to act on this information in an end-to-end fashion.&#0160; This is just not practical.&#0160; An alternative would be to add a protocol specific header to each frame that would allow for this identification to take place and this would probably work well.&#0160; However, since there is still only a single initiator that is shared across tenants, it doesn’t address the problem completely.</p>
<h3>Authentication (and encryption)</h3>
<p>Since there is only a single data plane element (e.g., an Initiator) that is shared between tenants on the same Hypervisor, there is no way to perform per-tenant data plane authentication.</p>
<p>Per-tenant encryption can be supported especially if you were to use application level encryption. &#0160;However, if you wanted to encrypt a particular tenants data by using an encryption appliance, you would need to be able to identify all traffic from a particular tenant. &#0160;As I described above, this could be done on a per LUN basis, but there are challenges with this approach. &#0160;</p>
<h3>Do not rely on Guest OS resident iSCSI initiators</h3>
<p>Since the initiators used to access storage run on the Hypervisor and not within an individual VM, this requirement is met by topology 1.</p>
<h2>Topology 1 summary</h2>
<p>With the exception of VVOLs, topology 1 is being used by many Enterprise customers today and works completely fine for <strong>many</strong>&#0160;Enterprise applications. &#0160;However, as I described in the <a href="/brasstacks/an-introduction-to-virtual-storage-networks/" target="_self">VSN overview post</a>, Service Provider environments are fundamentally different and a much higher priority is placed on support for multi-tenancy in general. &#0160;Since&#0160;topology 1 is unable to meet most of the multi-tenant storage requirements identified, I think it usefulness in Service Provider environments is minimal. &#0160;Next I’ll explain a topology that could meet all of the multi-tenant storage requirements and that may prove to be useful for applications that require an increased level of isolation. &#0160;</p>
<h2>Topology 2</h2>
<p>Topology 2 is similar to Topology 1 with a few “minor” changes that essentially allow each tenant to have a data plane personality that is separate from other tenants.&#0160; I’ll describe each of these changes and how they impact the specified requirement below; for now just know that these changes are:</p>
<ol>
<li>one or more initiators per tenant,</li>
<li>a per tenant I/O Monitor (IOM) module, and</li>
<li>a Traffic Shaper entity that ensures a tenant does not consume more bandwidth than has been allocated to it.&#0160;&#0160;&#0160;</li>
</ol>
<p>&#0160; <a class="asset-img-link" href="/brasstacks/virtual-storage-networks-part-3-multi-tenant-capable-topologies/6a013487ed263f970c01a73da95552970d.jpg" style="display: inline;"><img alt="Two" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01a73da95552970d image-full img-responsive" src="/brasstacks/virtual-storage-networks-part-3-multi-tenant-capable-topologies/6a013487ed263f970c01a73da95552970d.jpg" title="Two" /></a></p>
<h3>Satisfying Storage requirements</h3>
<p>As was done with topology 1, I’ll go through each of the multi-tenant storage requirements and discuss how topology 2 does or does not meet each requirement.&#0160;&#0160; &#0160;</p>
<h3>Namespace Isolation</h3>
<p>This requirement is satisfied by Topology 2.&#0160; This of course assumes each iSCSI initiator resides in its own namespace (e.g., <a href="http://blog.scottlowe.org/2013/09/04/introducing-linux-network-namespaces/" target="_self">network</a> and iSCSI namespaces).&#0160; Each iSCSI initiator can be exposed via multiple network interfaces with each attached to a tenant specific Virtual Network.&#0160; This Virtual Network could be a VLAN or another Virtual Network type (e.g., overlay based).</p>
<h3>Prevent noisy neighbor problems</h3>
<p>This requirement is theoretically met by Topology 2.&#0160; I say theoretically because the introduction of a Traffic Shaper (TS) to the network edge could ensure that a given tenant does not consume more transmit bandwidth than has been allocated to it.&#0160; There are a couple of challenges with this approach that would still need to be sorted out and the big one for me is the resource scheduler function.&#0160; I mean consider a situation where you have allocated 5000 IOPS to a tenant.&#0160; You would need to be able to share the IOPS fairly between all VMs whether or not all VMs are located on the same hypervisor. &#0160;In any case, by performing the same TS function at the VSA and by using a non-blocking region of the network, we’re probably about as close to a true end to end bandwidth &quot;guarantee&quot; as we’re going to get for the foreseeable future. &#0160;Note, if you decide to use a lossless protocol (e.g., FC, FCoE), congestion spreading could still cause cross-tenant issues.&#0160; This would be a great area for T11&#39;s FC-NWSG (Fibre Channel New Work Study Group) to investigate.</p>
<h3>Provide Bandwidth, IOPS and Response Time guarantees</h3>
<p>This requirement is satisfied by topology 2.&#0160; As I described above, I’d want to validate that the TS functionality solves the Bandwidth allocation issue.&#0160; That having been said, since each tenant utilizes a tenant specific iSCSI initiator, IOPS and Response Time could be allocated and monitored on a per tenant basis.&#0160; The IOM would ensure that the effective IOPS and RT being experienced by the end users remain within tolerances.&#0160; If this is not the case, the remediation steps I mentioned earlier could be used to resolve both acute and chronic IOPS and RT related issues.&#0160; &#0160;</p>
<h3>Tenant Traffic Identification and Storage Network Service Insertion</h3>
<p>This requirement is satisfied by topology 2.&#0160; Again, each tenant utilizes a unique iSCSI initiator and as a result each tenant can be isolated onto a specific Virtual Network which could be rerouted through devices that provide per tenant storage services (e.g. in flight encryption).&#0160; VVOLs (or alternatively one LU per VM) will still be needed because these allow for per VM actions to be performed on the array themselves.</p>
<h3>Authentication (and encryption)</h3>
<p>This requirement is satisfied by topology 2.&#0160; Each tenant can be authenticated individually on the data plane.&#0160; Also, as described above, since the tenant traffic can be easily identified it would be possible to pass it (and only it) through a storage service appliance (e.g. in flight encryption) without impacting other flows.&#0160; Finally, as I mentioned earlier when I introduced the concept of an IOM, if the IOM included an encryption function, all data belonging to a tenant could be encrypted at the IOM before it leaves the tenant container.</p>
<h3>Do not rely on Guest OS resident iSCSI initiators</h3>
<p>Since the initiators used to access storage run on the Hypervisor and not within an individual VM, this requirement is also met by topology 2.</p>
<h2>Topology 2 summary</h2>
<p>From a multi-tenant storage point of view, I think topology 2 has the potential to meet all of the requirements identified.&#0160; That having been said, the majority of these concepts are still at an advanced development stage.&#0160; If you’re interested in utilizing any of these concepts or think we’ve missed something, I&#39;d like to hear from you.</p>
<h2>Topology 2 – Additional information</h2>
<p>As I just mentioned, topology 2 is in what we’d refer to as the Advanced Development stage.&#0160; To give you a better idea of what this means, I’ve included a couple of diagrams that illustrate the topology we used to validate the network namespace isolation requirement. &#0160; Keep in mind, this is the topology that we&#39;re using for Proof of Concept (PoC) testing, this is not necessarily the topology that this functionality requires. &#0160;</p>
<p>&#0160; <a class="asset-img-link" href="/brasstacks/virtual-storage-networks-part-3-multi-tenant-capable-topologies/6a013487ed263f970c01a5119e480b970c.jpg" style="display: inline;"><img alt="Three" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01a5119e480b970c image-full img-responsive" src="/brasstacks/virtual-storage-networks-part-3-multi-tenant-capable-topologies/6a013487ed263f970c01a5119e480b970c.jpg" title="Three" /></a></p>
<p>&#0160; <a class="asset-img-link" href="/brasstacks/virtual-storage-networks-part-3-multi-tenant-capable-topologies/6a013487ed263f970c01a5119e481b970c.jpg" style="display: inline;"><img alt="Four" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01a5119e481b970c image-full img-responsive" src="/brasstacks/virtual-storage-networks-part-3-multi-tenant-capable-topologies/6a013487ed263f970c01a5119e481b970c.jpg" title="Four" /></a></p>
<p>Some of the PoC topology specifics are:</p>
<ul>
<li>Ubuntu 13.10 was used for the “hypervisor”</li>
<li>Two tenants (e.g., T1 and T2) were simulated using Linux containers (LXC)
<ul>
<li>Each container had its own management interface that was intended to be used by a Cloud or Infrastructure admin to configure tenant elements.&#0160; Because this management interface was intended to be accessed remotely (via br0 and the LAN) it needed to have a unique IP Address.</li>
<li>Each container had File (storage) interface.&#0160;</li>
<ul>
<li>Note that the IP Address was the same on both File interfaces.&#0160; These IPs didn’t need to be the same, but that was the point of the test; to validate namespace isolation was working for File interfaces in each container.&#0160;</li>
<li>These File interfaces were not assigned to a particular VM, just to the container.</li>
<li>These File interfaces were connected to a bridge and then this bridge was connected to a particular VLAN.&#0160; Again, we could have (and have in the past) used an overlay Virtual Network instead of a VLAN.&#0160;</li>
</ul>
<li>Two KVM based VMs we’re instantiated inside of each container
<ul>
<li>This caused all kinds of issues with AppArmor.&#0160; If you’re going to try this be prepared to put all of the LXC related AppArmor profiles into complain mode.</li>
<li>Each VM had a public interface that was intended to be used for remote access.</li>
<li>Each VM also had a storage interface.&#0160; We also could have used duplicate IP Addresses (e.g., T1-VM3 = 192.168.61.110 and T2-VM3 = 192.168.61.110)</li>
</ul>
</li>
<li>We had also planned to do some testing with iSCSI in this environment but we ran into an issue related to a lack of support for multiple network namespaces that prevented us from moving forward with it at this time.&#0160; I believe someone else ran into&#0160;<a href="https://bugs.launchpad.net/ubuntu/+source/lxc/+bug/1226855" target="_self">this bug</a>&#0160;as well.</li>
</ul>
</li>
</ul>
<h2>Conclusion</h2>
<p>So this was a lot of information to try and cover in one post and then relate to the other posts in the series. &#0160;With this in mind, the key points of the blog series up to this point are:</p>
<ul>
<li>Service Provider and Enterprise environments are fundamentally different (as discussed in the&#0160;<a href="/brasstacks/an-introduction-to-virtual-storage-networks/" target="_self">VSN overview post</a>).</li>
<li>Topology 1 is widely used today by many Enterprise customers but it does not provide data plane isolation between tenants and this is a feature which could be very useful in Service Provider environments.</li>
<li>Topology 2 allows for data plane isolation between tenants, but a lot of work still needs to be done to work through the details... However, we&#39;re working on it and would value any inputs..</li>
<li>Regardless of the need for data plane isolation, both types of customers are asking for the ability to automate storage provisioning tasks</li>
<li>A big part of the storage provisioning process is establishing connectivity between storage consumers and producers.</li>
<li>We would like to automate the establishment of connectivity between the storage entities to facilitate the creation of storage service compositions. &#0160; &#0160;</li>
</ul>
<h2>Next time... Connectivity Automation</h2>
<p>In part 4 of this series I&#39;ll define what I mean by Connectivity Automation and describe how it can be applied to the topologies I introduced in this post.</p>
<p>Thanks for reading!</p>
