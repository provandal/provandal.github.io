---
title: "The IaaS Missing Link"
pubDate: 2017-11-30
postedAt: "02:56 PM"
description: "The beginning Almost exactly two years ago, a small group of us (including Alan Rajapa and Massarrah Tannous) participated in a “Hack Attack” that was being run by one of the Storage Platform teams within EMC. Our concept was simple; we were going to completely eliminate the manual storage provisioning..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2017/11/the-iaas-missing-link.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250911172147/https://brasstacksblog.typepad.com/brass-tacks/2017/11/the-iaas-missing-link.html"
pdf: "/brasstacks/the-iaas-missing-link/the-iaas-missing-link.pdf"
comments: []
---

<p><span style="font-size: 14pt;">The beginning</span></p>
<p>Almost exactly two years ago, a small group of us (including Alan Rajapa and Massarrah Tannous) participated in a “Hack Attack” that was being run by one of the Storage Platform teams within EMC.&#0160;</p>
<p>Our concept was simple; we were going to <strong>completely eliminate the manual storage provisioning steps required to expose EMC Array based storage to an OpenStack instance</strong>.</p>
<p>If you know anything about OpenStack and Cinder, you understand why we&#39;d want to do this.&#0160; Back then, manually adding a storage array “backend” to OpenStack required about 17 steps per compute (server) instance.&#0160; Not only that, the amount of information you needed to collect from each backend (Storage array) required you to know EXACTLY what you were doing.&#0160;</p>
<p>Very few people did.&#0160;</p>
<p>As a result, we were hearing about failed OpenStack implementations and frustrated customers asking “why does this need to be so HARD??”.</p>
<p>We felt that it didn’t need to be.</p>
<p>In fact, we were pretty sure that we could accomplish our goal using open source tools and very little additional development would be required.&#0160;</p>
<p>In the end, I think we were wildly successful with our concept of “Zero Touch Storage Provisioning” (ZTSP) and actually won third place in the event.&#0160;</p>
<p>Now, you’re probably wondering why you’ve never heard of this project (at least on this blog) and I’ll just say that the ZTSP backstory along with the TDZ backstory will have to wait for another day.</p>
<p>In any case, these experiences HAVE led to a ton of insights that I’ll be talking about over the next few blog posts.&#0160; One of the biggest discoveries (for me) was the existence of an IaaS “Missing Link”.</p>
<p>But before we go there, I’ll describe Zero Touch Storage Provisioning (ZTSP) and then I’ll use this concept to help describe the missing link.</p>
<h2>Zero Touch Storage Provisioning (ZTSP)</h2>
<p>The following diagram shows the typical configuration we were testing with at that time.&#0160; In consisted of:</p>
<ol>
<li>An OpenStack controller that was running a multitude of OpenStack services including the Horizon UI. Horizon was an apache based GUI that supports end users allocating storage to VMs (amongst other things).</li>
<li>A storage array that supports <a class="zem_slink" href="https://en.wikipedia.org/wiki/ISCSI" rel="wikipedia noopener noreferrer" target="_blank" title="ISCSI">iSCSI</a></li>
<li>Three compute nodes that were each running the <a class="zem_slink" href="https://en.wikipedia.org/wiki/OpenStack" rel="wikipedia noopener noreferrer" target="_blank" title="OpenStack">OpenStack Cinder</a> Service</li>
<li>A management network (blue dashed lines)</li>
<li>A data plane network (black solid lines) &#0160;</li>
</ol>
<p><a class="asset-img-link" href="/brasstacks/the-iaas-missing-link/6a013487ed263f970c01b8d2c32092970c.jpg" style="display: inline;"><img alt="Pic1" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b8d2c32092970c image-full img-responsive" src="/brasstacks/the-iaas-missing-link/6a013487ed263f970c01b8d2c32092970c.jpg" title="Pic1" /></a></p>
<p>In order to be able to provision storage (on an EMC based storage array) and expose it to a VM (running on one of the Hosts running Cinder), you needed to follow a fairly complicated process that, at least at one point, required 17 configuration steps.&#0160; These steps included creating a storage group on the array, collecting information about the array and the storage group from the array, masking the host to see the storage group on the array and then once this work had been done you had to go to each host and configure the cinder.conf file to create a storage “backend”.&#0160; This was a tedious, time consuming and error prone process that seemed to be getting in the way of customer adoption.&#0160;</p>
<p>Also, about this time, VMware VSAN was really starting to get some attention.&#0160; In fact, I had set it up in the lab and was completely blown away by the experience.&#0160; It was just SO simple to use and represented a quantum leap forward in simplicity for storage consumers.&#0160; I found it such a great experience that I set out to try and reproduce the VSAN storage consumption experience with traditional storage arrays and hence the idea of Zero Touch Storage Provisioning we born.&#0160; It was shortly after this that we received the invite to participate in the Hack Attack and so after discussing it with the team we decided to give it a shot.</p>
<p>We quickly realized that the storage provisioning problem we were trying to solve could be broken down into three parts:</p>
<ol>
<li>Discovery – Determine when a new storage array was attached to the data plane network.</li>
<li>Configuration - Determine what information needed to be put into the cinder.conf file.</li>
<li>Delivery:
<ol style="list-style-type: lower-alpha;">
<li>Determine how to get the information into the cinder.conf file on the hosts and then refresh the cinder service.</li>
<li>Determine how to refresh the Horizon service on the control node in order for it to pick up the new storage backend and display it to the end user.</li>
</ol>
</li>
</ol>
<p>We also quickly realized that Puppet was a good choice to handle part 3 (Delivery).&#0160; We would just create a “Gold copy” of the cinder.conf on the Puppet master and then allow the individual hosts to detect the change, download the new “Gold copy” of the cinder.conf and then refresh the cinder service.&#0160; With the exception of actually populating the contents of the “Gold copy” of the cinder.conf, all of these steps were almost trivial to accomplish with puppet.&#0160;</p>
<p>Part 1 (Discovery) was also very simple to solve, at least on paper.&#0160; Our plan was to use the <a class="zem_slink" href="https://en.wikipedia.org/wiki/Link_Layer_Discovery_Protocol" rel="wikipedia noopener noreferrer" target="_blank" title="Link Layer Discovery Protocol">Link Layer Discovery Protocol</a> (LLDP) and to have the data plane interfaces on the array populate the LLDP packets being transmitted with just enough information to allow something (e.g., our controller) to detect that an array had been connected to the network.&#0160; It turns out that getting the information to the switch via LLDP was pretty straight forward but in order to detect that a new array had been added, we had to choose to either poll for LLDP information or use an asynchronous notification mechanism.&#0160; We chose the latter and used SNMP for this purpose.&#0160;</p>
<p>Part 2 (Configuration) required a bit more work but again, nothing too complicated.&#0160; Our plan was to use the information provided in the LLDP packet to login to the array’s management interface, configure the required storage pools, update the masking and then collect the appropriate information such that we could update the “Gold copy” of the cinder.conf.</p>
<h2>Bringing it all together</h2>
<p>With the above plan in place, here’s what we actually ended up doing during the Hack Attack.</p>
<h3>Pre-requisites</h3>
<ol>
<li>We updated the array firmware so that it would transmit LLDP packets that contained two pieces of information:
<ol>
<li>The <a class="zem_slink" href="https://en.wikipedia.org/wiki/MAC_address" rel="wikipedia noopener noreferrer" target="_blank" title="MAC address">MAC Address</a> of the 10G interface</li>
<li>The IP Address of the array’s management interface</li>
</ol>
</li>
<li>We created a ZTSP controller that contained:
<ol>
<li>Puppet</li>
<li>A cinder.conf publisher</li>
<li>An SNMP_Discovery.py that we ran as a daemon and contained:
<ol>
<li>An SNMP Trap listener</li>
<li>An SNMP query function (to retrieve LLDP information from the switches)</li>
</ol>
</li>
<li>A Storage API consumer</li>
<li>Credentials for the storage array. They were in plain text but we could have used something like vault for this (and have since).&#0160;</li>
</ol>
</li>
<li>Each switch needed to have the ZTSP Controller’s IP Address added as a trap recipient</li>
<li>Puppet needed to be installed and configured.</li>
</ol>
<h3>The process</h3>
<p>The configuration process we created is shown below and explained in more detail in the text that follows.</p>
<p>&#0160; <a class="asset-img-link" href="/brasstacks/the-iaas-missing-link/6a013487ed263f970c01b8d2c320cd970c.jpg" style="display: inline;"><img alt="Pic2" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b8d2c320cd970c image-full img-responsive" src="/brasstacks/the-iaas-missing-link/6a013487ed263f970c01b8d2c320cd970c.jpg" title="Pic2" /></a></p>
<ol>
<li>The 10G interface on the array was attached to a port on the leaf switch. As soon as the link was up the interface started to transmit LLDP packets that contained the MAC Address of the 10G data plane interface (that was just attached) and the IP Address of the Array&#39;s management interface.</li>
<li>As soon as the port on the switch changed state, an SNMP trap was sent from the switch to the ZTSP controller and was handled by our trap listener.</li>
<li>The ZTSP controller would retrieve the LLDP information from the switch.</li>
<li>Using IP Address from the LLDP packet that was retrieved in step 3 and the storage management interface credentials that had been stored in the controller ahead of time, the ZTSP controller would login, create a storage group, update the masking and then collect the information we needed to update the “Gold copy” of the cinder.conf.</li>
<li>We created/updated the “Gold copy” of the cinder.conf</li>
<li>Puppet took care of the delivery of the cinder.conf to each node as well as the need to refresh the cinder service on each compute node as well as the horizon UI on the control node.</li>
</ol>
<p>With this functionality in place, all of the OpenStack specific configuration steps were eliminated and we declared success!&#0160;</p>
<h2>The IaaS missing link</h2>
<p>Although our Proof of Concept was a huge success and we were able to demonstrate exactly what we set out to do, we noticed that “completely automating the consumption of storage” and “completely automating the configuration of Cinder specific configuration parameters” were totally different things.&#0160; In fact, the work we had done during our PoC represented the latter and was really only the “easy” stuff.&#0160; This work is shown in the “Services” layer below.&#0160; The really hard stuff, like <a href="/brasstacks/how-to-determine-a-switchs-role-in-a-clos-network-with-mlagd-leaves/">configuring an IP Network</a> or configuring end-to-end connectivity for iSCSI was much harder and fell into an area that I refer to as the “IaaS missing link.”&#0160; &#0160;</p>
<p><a class="asset-img-link" href="/brasstacks/the-iaas-missing-link/6a013487ed263f970c01b8d2c320dd970c.jpg" style="display: inline;"><img alt="Pic3" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b8d2c320dd970c image-full img-responsive" src="/brasstacks/the-iaas-missing-link/6a013487ed263f970c01b8d2c320dd970c.jpg" title="Pic3" /></a></p>
<p>I’ll provide much more information about the IaaS missing link in my next blog post.&#0160;</p>
<p>Thanks for reading!</p>
