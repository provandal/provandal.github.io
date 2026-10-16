---
title: "A thought experiment - The Universal Fabric"
pubDate: 2012-02-20
postedAt: "07:34 PM"
description: "This post is in response to a post by Scott Lowe, another post by Maish Saidel-Keesing and his reaction to TDZ as a potential solution to satisfy his requirements for a “dvFabric”. Maish’s statement via twitter: “…but this (TDZ) only covers block storage. What about NAS?” honestly set me back..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2012/02/a-thought-experiment-the-universal-fabric.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250911115856/https://brasstacksblog.typepad.com/brass-tacks/2012/02/a-thought-experiment-the-universal-fabric.html"
pdf: "/brasstacks/a-thought-experiment-the-universal-fabric/a-thought-experiment-the-universal-fabric.pdf"
comments:
  - author: "Simon Gordon"
    date: "05/19/2012 at 02:20 AM"
    html: |-
      <p>Did you know that iSNS has a (maybe slightly flawed) fc model built in to it ? We&#39;ve discussed some similar ideas over here more than once, and there is a lot of sense to what you say.  Some small and subtle changes in a few places would be goodness.  With servers and indeed storage being increasingly multiprotocol there is even more reason why this makes sense no matter the exact mechanisms you would use. IMHO the biggest issue here is that the politics within one standard body is tricky enough, but the politics across two or three standards bodies makes it hard to get some of this stuff done which I think is a shame.</p>
  - author: "Erik Smith"
    date: "05/19/2012 at 08:57 AM"
    html: |-
      <p>Thanks Simon, actually, I&#39;ve decided to try and avoid the politics with the standards bodies for now and try something different this time.  Stay tuned.. </p>
---

<p>This post is in response to a <a href="http://blog.scottlowe.org/2012/02/08/thinking-out-loud-is-a-dvfabric-closer-than-we-think/" target="_self">post by Scott Lowe</a>, another <a href="https://technodrone.blogspot.com/2012/02/my-wish-for-dvfabric-dvswitch-for.html" target="_self">post by Maish Saidel-Keesing</a> and his reaction to <a href="/brasstacks/introducing-target-driven-zoning-tdz/" target="_self">TDZ</a> as a potential solution to satisfy his requirements for a “dvFabric”.&#0160; Maish’s statement via twitter:</p>
<p>“…but this (TDZ) only covers block storage.&#0160; What about NAS?”</p>
<p>honestly set me back on my heels a bit.&#0160; My first reaction was “TDZ and NAS are orthogonal and will operate independently from one another”, but as I thought about his point some more, I realized that while FC/FCoE and NAS are completely different protocols, why can’t a “TDZ like” approach apply to both?&#0160; And this led to another question, why should the solution be limited to VMware users?&#0160; Then I figured since we’re thinking “outside of the box” why not think&#0160;<strong>way outside</strong> of the box…</p>
<p>Before I get too much further along, I feel it’s important to acknowledge the contributions of Mark Lippitt, Jack Harwood, David Black, David Cohen, Wayne Berthiaume and Mugdha Kulkarni especially in the iSCSI portion of this post.&#0160; I have a hard time figuring out exactly where their ideas end and mine begin but suffice it to say much of what I’m describing came about due to some amount of collaboration with this team.</p>
<h2>I need more storage!</h2>
<p>When I setup a new configuration, the <a href="/brasstacks/fc-and-fcoe-versus-iscsi-network-centric-versus-end-node-centric-provisioning/" target="_self">steps that I have to perform</a> to make additional storage visible to the host vary based on the OS and protocol in use.&#0160; Perhaps it’s a bit obvious, but successfully performing these steps is not the goal, they are the means to an end. I’ll go out on a limb and say if there’s an easier way to accomplish the same set of tasks, it would be very interesting to almost everyone.&#0160; Breaking this idea down to its most basic component, you start with an&#0160;administrator who’s thinking “Oh, &lt;optional expletive&gt; I need more storage!”&#0160; <em>Actually, ideally, applications would automatically provision additional storage capacity as needed and notify the administrator that it was done, but I digress.</em>&#0160; My point is, the set of steps that the Administrators have to perform to provision the additional storage are, in reality, nothing more than obstacles getting in the way of the real goal of <strong>provisioning more storage</strong>.&#0160; Therefore, reducing the number of storage provisioning steps to be as close to zero as possible would be viewed as a good thing by end users.&#0160; If we can agree on this, then there are at least two general approaches to satisfying this requirement; I’ll refer to them as “top down” and “bottom up” (I know, not very original).</p>
<h2>Top down</h2>
<p>Top down is the idea of using a centralized “Controller” to configure the Compute, Network and Storage pools.&#0160; For more information on this kind of approach, check out <a href="http://openstack.org/" target="_self">OpenStack</a> and the numerous IaaS, PaaS offerings available today that meet this kind of requirement.&#0160; I’m a huge fan of OpenStack and I’m devoting a significant portion of my personal time getting to know it better (IOW, expect a post or two about it in the future).&#0160; However, one of my concerns about the OpenStack approach is&#0160;it&#39;s so radically different from what has been done traditionally.&#0160; I mean if you’re running a production data center today and are looking for a way to <strong>incrementally</strong> improve the efficiency of the storage provisioning process, you might look at something like OpenStack as a potential solution that has no business being anywhere near your production data center (for now).&#0160; That having been said, one example of how a top down approach could be used would be:</p>
<ol>
<li>The user interacts with the centralized controller to provision additional storage.&#0160; </li>
<li>The controller would then parse the users request, potentially apply some rules to the request and then interact with the host, network and storage to:<ol>
<li>Provision the storage and allow the host access to a certain number of LUNs</li>
<li>Configure the network to allow the host and storage to access each other</li>
<li>Point the host at the proper storage port</li>
</ol></li>
</ol>
<p>Long term I think this approach has a ton of potential to make our lives easier.</p>
<h2>Bottom up</h2>
<p>Bottom up is the idea of configuring one of the end devices and then using a centralized service to reduce the number of manual configuration steps required on the host, network and storage.&#0160; One example of this approach is <a href="/brasstacks/introducing-target-driven-zoning-tdz/" target="_self">TDZ (Target Driven Zoning)</a>.&#0160; Although TDZ was designed for to be used in an FC/FCoE environment, I’ll describe over the next few sections&#0160;how&#0160;the same concepts could be applied to iSCSI and NAS.&#0160; &#0160;</p>
<h3>FC/FCoE</h3>
<p>With the current version of TDZ, the basic idea is to extend existing (and proven) features and protocols to <strong>incrementally improve </strong>the FC/FCoE end users experience <strong>while minimizing risk</strong>.&#0160; It does this by allowing a storage administrator to specify which hosts have access to a certain set of LUNs (as is done today) with the incremental improvement being:</p>
<ol>
<li>the Storage port is allowed to “publish” a list of “allowed” hosts to a centralized point (the fabric zone server)</li>
<li>the FC/FCoE network elements use this list to automatically configure itself (update zoning) </li>
<li>the hosts automatically discover the correct storage (via RSCN)</li>
</ol>
<p>To make a long story short, the only change required to FC/FCoE to make this happen was the creation of the “peer zone”.&#0160; This very small change enabled a significant saving in terms of provisioning steps.</p>
<h3>iSCSI</h3>
<p>The same “TDZ like” approach could be applied to iSCSI with a couple of minor changes to the way the iSNS is used.&#0160; <em>Actually, first people would need to use the iSNS, but that’s another story…</em>&#0160; The following gives an overview of one possible way this could be done.</p>
<p>A couple of things to take note of before I begin:</p>
<ul>
<li>The following example assumes that DHCP option 43 (vendor specific) is being used in a manner similar to what is <a href="http://wiki.siemens-enterprise.com/wiki/VLAN_ID_Discovery_over_DHCP" target="_self">described here</a></li>
<li>To fully realize the benefits of this approach, a DHCP option specific to iSCSI-VLANs will be required</li>
<li>The diagrams in this section show the iSNS and DHCP servers embedded in the switch chassis.&#0160; I’ve only drawn it this way for convenience and they could just as easily be a centralized service running somewhere within the network.&#0160; The point is this solution isn’t limited to single switch topologies.</li>
<li>The switch will need to be administratively configured with:
<ul>
<li>at least two VLANs (e.g., 1 and 100) as shown in figure 1 (below)</li>
<li>The DHCP and iSNS servers will need to be enabled and accessible from the appropriate VLANs</li>
<li>The DHCP server will need to support something like the vendor specific option (option 43).
<ul>
<li>this option will need to return a list of VLANs that support iSCSI</li>
</ul>
</li>
<li>Each switch interface will need to be configured as a trunk port and the appropriate VLANs (e.g., 1 and 100) will need to be allowed on each of the interfaces </li>
</ul>
</li>
</ul>
<h3><a href="/brasstacks/a-thought-experiment-the-universal-fabric/6a013487ed263f970c0168e7b34dbf970c.jpg" style="display: inline;"><img alt="One" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0168e7b34dbf970c image-full" src="/brasstacks/a-thought-experiment-the-universal-fabric/6a013487ed263f970c0168e7b34dbf970c.jpg" title="One" /></a></h3>
<p><span style="text-decoration: underline;">iSCSI initiator configuration and registration</span></p>
<p>The iSCSI initiator interfaces will initialize as follows:</p>
<p><strong>Note:</strong> An “enable iSCSI” configuration parameter may need to be provided to prevent iSCSI discovery from being performed on inappropriate interfaces.&#0160; This overview assumes that such a configuration parameter has been provided and that eth0 (see figure 2) is configured to perform iSCSI Discovery.</p>
<p><strong>1.</strong> During boot, link initialization, etc, the server containing the iSCSI client will discover the DHCP server.&#0160; The discovery would be performed using the default VLAN and the server could request IP, subnet mask, gateway/router and a special parameter (option 43) that indicates the DHCP server should provide a list of VLANs that support iSCSI.&#0160; <em>If you&#39;re familiar with FIP VLAN Discovery, then you&#39;ll understand where this idea came from</em>.&#0160; &#0160;</p>
<p><strong>2. </strong>The DHCP server should respond with an IP Address, subnet mask, Gateway/Router, DNS (optional), and a list of VLANs that have been created for the purpose of supporting iSCSI (VLAN 100 in this case).</p>
<p><strong>Note:</strong> interface eth0 will be used for the sake of this example but this process&#0160;could be used on every &quot;ethx&quot; instance that has “iSCSI Discovery” enabled on it.</p>
<p><strong>3.</strong> The iSCSI Initiator should configure the IP Address, subnet mask, default gateway and DNS of eth0 to match what was returned from the DHCP Server. (Normal DHCP)</p>
<p><strong>4.</strong> A new “service” on the iSCSI Initiator should create one new interface for each iSCSI VLAN returned from the DHCP server.&#0160; These interfaces will have&#0160;the format of “ethx.y” where x is equal to the interface instance where the iSCSI VLANs were discovered and y is equal to the VLAN ID returned.&#0160; For example, “eth0.100” as shown in figure 2.</p>
<p><a href="/brasstacks/a-thought-experiment-the-universal-fabric/6a013487ed263f970c016762b16ac3970b.jpg" style="display: inline;"><img alt="Two" border="0" class="asset  asset-image at-xid-6a013487ed263f970c016762b16ac3970b image-full" src="/brasstacks/a-thought-experiment-the-universal-fabric/6a013487ed263f970c016762b16ac3970b.jpg" title="Two" /></a></p>
<p><strong>5.</strong> Once the iSCSI interfaces (e.g., eth0.100) have been created, DHCP discovery can be repeated on these interfaces with two exceptions:</p>
<ul>
<li>The iSCSI-VLAN option should not be specified. (since the iSCSI VLANs were already discovered)</li>
<li>DHCP option 83 (DHCP option for iSNS) should be specified. (iSNS discovery)</li>
</ul>
<p>&#0160;<a href="/brasstacks/a-thought-experiment-the-universal-fabric/6a013487ed263f970c016762b16b8d970b.jpg" style="display: inline;"><img alt="Three" border="0" class="asset  asset-image at-xid-6a013487ed263f970c016762b16b8d970b image-full" src="/brasstacks/a-thought-experiment-the-universal-fabric/6a013487ed263f970c016762b16b8d970b.jpg" title="Three" /></a></p>
<p><strong>6.</strong> After the iSCSI interfaces have been configured with the information returned from the DHCP Server, the iSNS Client on the iSCSI Client should register with the iSNS.&#0160; The information registered should include the IP Address and IQN.&#0160; The iSNS client should also register for SCN.</p>
<p><strong>7.</strong> After registering with the iSNS, the iSCSI initiator should query the iSNS for iSCSI Targets.</p>
<p><strong>8.</strong> For each iSCSI target returned by the iSNS, the iSCSI initiator should perform&#0160;login and SCSI Discovery (report LUNS, etc).</p>
<p>Note: At this point in our example, since the iSCSI Target is not yet registered with the iSNS, no iSCSI targets will be returned.</p>
<p><span style="text-decoration: underline;">iSCSI Target configuration and registration</span></p>
<p><strong>1.</strong> In order to facilitate the automation of the network provisioning process, each target will need to register information with the iSNS.&#0160; This information should include:</p>
<ul>
<li>the same type of information that was registered by the Initiator; and </li>
<li>will also include the list of iSCSI initiators that should have access to the iSCSI Target (if any).&#0160; This will be accomplished through the use of the DDReg message.&#0160;&#0160;&#0160;&#0160;&#0160;&#0160; </li>
</ul>
<p><strong>2.</strong> Assuming the target has been configured to allow access to the iSCSI initiator, the initialization process shall be the same as defined for the iSCSI initiator with the following exceptions:</p>
<ul>
<li>The iSCSI Target will need to be configured as a management station and, as defined in RFC 4171:
<ul>
<li>register as a control node</li>
<li>register for management SCNs</li>
<li>register its own Login Control list using the DDReg message and listing the iSCSI name of each initiator to be registered in the target&#39;s DD</li>
<li>query for the discovery domain set (DDS) name/ID and then add their DD to that DDS.</li>
</ul>
</li>
</ul>
<p>Figure 4 shows the topology after the target has completed interface initialization.</p>
<p><a href="/brasstacks/a-thought-experiment-the-universal-fabric/6a013487ed263f970c0168e7b3509f970c.jpg" style="display: inline;"><img alt="Four" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0168e7b3509f970c image-full" src="/brasstacks/a-thought-experiment-the-universal-fabric/6a013487ed263f970c0168e7b3509f970c.jpg" title="Four" /></a></p>
<p><span style="text-decoration: underline;">iSCSI initiator discovery of targets after SCN</span></p>
<p><strong>1.</strong> Once the iSCSI target has completed registration, the iSNS would transmit SCN to the iSCSI Initiator</p>
<p><strong>2.</strong> Upon reception of SCN from the iSNS, the iSCSI initiator should query the iSNS for iSCSI Targets.</p>
<p><strong>3.</strong> For each iSCSI target returned by the iSNS, perform login and SCSI Discovery.</p>
<h3>NAS</h3>
<p>I believe this same approach could be applied to NAS via something like Autofs (although I haven’t completely worked through exactly how this would be done).&#0160; It would require a centralized point for the NFS server to publish mount points / associated list of clients (users, IPs, subnets?) that were configured to have access these mount points.&#0160; I believe this can be done via NIS or LDAP but as I’ve discovered with iSCSI, I wouldn’t at all be surprised to find that a few changes would be required to existing implementations in order to get this to work.&#0160; By the way, if anyone reading this is interested in thinking outside of the box with me and has NAS expertise, I’d really like to hear from you!</p>
<h2>The Universal Fabric</h2>
<p>If you consider the discovery automation functions that I’ve described over the past couple of sections, you’ve probably noticed a pattern.&#0160; In each case I propose extensions to existing technologies/protocols that will allow for <strong>incremental improvements</strong> to each individual technology.&#0160; While it’s true that these enhancements require additional &quot;up front&quot; work to be done by the administrator, these additional steps will&#0160;only need to be performed once.&#0160; So let’s assume for a minute that all of the infrastructure components have been configured and you no longer need to worry about those configuration steps on an ongoing basis.&#0160; What you are left with is a simple way to provision and re-provision storage in one <strong>protocol independent</strong> way.</p>
<p><a href="/brasstacks/a-thought-experiment-the-universal-fabric/6a013487ed263f970c0168e7b3512f970c.jpg" style="display: inline;"><img alt="Five" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0168e7b3512f970c image-full" src="/brasstacks/a-thought-experiment-the-universal-fabric/6a013487ed263f970c0168e7b3512f970c.jpg" title="Five" /></a></p>
<p>You would simply:</p>
<p><strong>1.</strong> Connect to the storage array / NAS head and provision storage (LUNs / mount points)</p>
<p><strong>2.</strong> The storage publishes this information in a protocol specific way:</p>
<ul>
<li>For FC and FCoE, use <a href="/brasstacks/introducing-target-driven-zoning-tdz/" target="_self">TDZ</a></li>
<li>For iSCSI, use the iSNS as I described above.</li>
<li>For NAS, maybe NIS/LDAP would be appropriate.</li>
</ul>
<p><strong>3.</strong> The host could then automatically discover the storage that has been made available to it using&#0160;any combination of the above three methods:</p>
<ul>
<li>For FC and FCoE, an RSCN would prompt the host to perform discovery.</li>
<li>For iSCSI, SCN would prompt the host to perform discovery.</li>
<li>For NAS, Autofs could be set to poll the NIS/LDAP server (probably not a good idea) or the user could kick off a simple discovery script.</li>
</ul>
<p>It’s important to point out that, as is the case with TDZ, the presence of these “helper” functions would not impede normal discovery / provisioning if that is what you wanted to do with one or all of the protocols.&#0160; In other words, this should be completely backward compatible with what is being done in your environment today because these functions&#0160;merely <strong>extend</strong> what is already being done.</p>
<p>Thoughts?</p>
<p>Thanks for reading!</p>
