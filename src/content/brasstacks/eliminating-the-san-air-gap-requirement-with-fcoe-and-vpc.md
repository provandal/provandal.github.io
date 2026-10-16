---
title: "Eliminating the SAN “Air-gap” requirement with FCoE and vPC"
pubDate: 2011-05-08
postedAt: "12:25 AM"
description: "While reading J Metz’s blog post, I noticed a comment from one of my friends at Brocade that made reference to an “Air-gap fabric” requirement and this prompted me to provide a response of my own. In my response, I briefly outlined not only what I’ll be writing about in..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2011/05/eliminating-the-san-air-gap-requirement-with-fcoe-and-vpc.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250911133637/https://brasstacksblog.typepad.com/brass-tacks/2011/05/eliminating-the-san-air-gap-requirement-with-fcoe-and-vpc.html"
pdf: "/brasstacks/eliminating-the-san-air-gap-requirement-with-fcoe-and-vpc/eliminating-the-san-air-gap-requirement-with-fcoe-and-vpc.pdf"
comments:
  - author: "BRCDbreams"
    date: "05/09/2011 at 01:33 PM"
    html: |-
      <p>Erik,</p>
      <p>First, full disclosuer, I work for Brocade.</p>
      <p>Thanks for showing this implementation of FCoE isolation.  As I look at this, I think an argument can be made that in a lot of ways the isolation afforded is reminiscent of the isolation achived when using FC routing with multiple FC fabrics.  With FC routing, each fabric control plane (and zoning and other policies) remains independent so Mr. Murphy-based configuration errors can&#39;t propogate beyond a single fabric.  A good thing.</p>
      <p>For those reasons, FC routers, properly implemented, are seen as preserving the air gap architecture for fibre channel fabrics. <br />
      I&#39;d appreciate your thoughts on that.</p>
      <p>And, indeed simplifing configuration steps would be a virtue, so I&#39;m interested in your experience with the Brocade VCS Ethernet fabric when you test that.</p>
  - author: "BRCDbreams"
    date: "05/09/2011 at 01:57 PM"
    html: |-
      <p>Erik,</p>
      <p>And one other point I forgot to add to my earlier comment.  I think my argument about FC routing preserving the air gap for the control plane meant that FC routing preserved the the air gap design goal of more than one independent control plan for storage traffic.  </p>
      <p>IF you agree with that, AND, IF you further think your design for FCoE w/ vPC provides at least two independent control plans for FCoE traffic, then I&#39;d say the title of your article would become &quot;Emulating the SAN air gap for FCoE with vPC&quot;.</p>
      <p>Last, can vPC support more than 2 switches as we can with FC Routing? If so, that would provide good scalability.</p>
  - author: "Erik Smith"
    date: "05/10/2011 at 01:09 AM"
    html: |-
      <p>Hi Brook, interesting point about FC Routing.  I had originally considered including that concept to support my claim about vPC and VCS, but it opens a can of worms that I haven&#39;t fully thought through let alone tested in the lab.</p>
      <p>If we are talking about a stand alone Brocade FC Router that contains EX_Ports, then with Brocade&#39;s implementation, I am fairly comfortable with the idea since the EX_Port was described to me by one of your Engineers&#39; as a light E_Port that accepts configuration information from the fabric.  Thinking about it now, the exceptions are probably SW_RSCNs and probably E_Port specific frames like HLO, etc but I&#39;m sure you know more so than I.  In any case, given that the EX_Ports aren&#39;t pushing configuration information to both fabrics, I&#39;m OK with the idea but would want to get into the lab and validate before signing off on the idea completely.  </p>
      <p>With the other implementations, or when the routing capability is build into one or both of the switches that are participating in the fabric, I&#39;m not ready to sign off on the concept yet.  To be completely honest, my hesitation is due more to a lack of knowledge about the internals of Brocade&#39;s Integrated Routing and Cisco&#39;s IVR rather than specific knowledge about any particular problem.  That having been said, I&#39;d be open to the idea if either of them truly isolates the SANs from one another.  </p>
      <p>To answer your other questions, vPC is currently limited to two switches and I&#39;m not sure if this will change or not going forward.  </p>
      <p>If we only disagree about the title of the blog post, I think we&#39;re in pretty good shape!!</p>
---

<p style="text-align: left;">While reading <a href="http://blogs.cisco.com/datacenter/to-tell-the-truth-multihop-fcoe/" target="_self">J Metz’s blog post</a>, I noticed a comment from one of my friends at Brocade that made reference to an “Air-gap fabric” requirement and this prompted me to provide a response of my own.&#0160; In my response, I briefly outlined not only what I’ll be writing about in this post, but also what I’ll be discussing during my EMC World presentation next week.&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;</p>
<p>The “Air-gap fabric” requirement basically states that if two FC fabrics are used to create a redundant FC fabric topology, the fabrics should be completely (physically and logically) isolated from one another, or in other words, separated by an air gap.&#0160; To be fair, until recently, I was a proponent of this approach (at EMC, we call it SAN A / SAN B) and I probably would have treated suggestions to break this best practice with contempt…&#0160; However, after having had the opportunity to configure and test vPC in our lab and see first hand the benefits it can provide, I’ve been thinking that I need to revise my stance slightly, at least when it comes to the definition of <strong>logical isolation</strong>.</p>
<p>For those of you who haven’t had a chance to use it, vPC or virtual Port Channel allows for two Cisco Ethernet switches to appear as a single physical chassis to a third device such as a host.&#0160; In the example shown below, Ethernet Switch / FCF 1A and 1B have been configured to be members of the same vPC domain and have been directly connected together via a vPC peer link.&#0160; The NIC/CNA connections from the host are each connected to a different switch and the switch ports they are attached to have been configured to be a part of the same virtual Port Channel.&#0160; Once this is done, the switch will appear to the host as a single chassis from a Layer 2 Ethernet (not including FCoE) perspective.</p>
<p><a href="/brasstacks/eliminating-the-san-air-gap-requirement-with-fcoe-and-vpc/6a013487ed263f970c0154322cd474970c.jpg" style="display: inline;"><img alt="VPC" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0154322cd474970c image-full" src="/brasstacks/eliminating-the-san-air-gap-requirement-with-fcoe-and-vpc/6a013487ed263f970c0154322cd474970c.jpg" title="VPC" /></a>&#0160;</p>
<p style="text-align: center;"><strong>Figure 1</strong>&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;</p>
<p>This is a very powerful concept because it allows a host to use active/active NIC teaming (or bonding with Linux) while still being connected to two <strong>physically</strong> separate switches thus avoiding a single point of failure due to a hardware malfunction.&#0160; Another nice feature of vPC is that since FCoE Frames are explicitly prohibited from crossing the vPC peer link, it allows the SANs to remain <strong>logically isolated</strong> preventing not only a single point of failure due to a software bug in the FC code but also preventing a loss of connectivity due to a well intentioned but ultimately misguided attempt to make an administrative change to something like FC fabric zoning.&#0160;</p>
<p>When I set this configuration up in the lab I noticed a number of interesting things:</p>
<ul>
<li>First was the fact that even though I had created a team and only had a single vNIC, the storage stacks (FCoE functionality) on each CNA remained separate from one another, see figure 2 below.&#0160; This wasn’t actually surprising but the fact that it was done this way allows our multi-pathing software (PowerPath) to continue to function normally.</li>
</ul>
<p style="text-align: center;"><a href="/brasstacks/eliminating-the-san-air-gap-requirement-with-fcoe-and-vpc/6a013487ed263f970c01538e5a02c1970b.jpg" style="display: inline;"><img alt="Figure2" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01538e5a02c1970b" src="/brasstacks/eliminating-the-san-air-gap-requirement-with-fcoe-and-vpc/6a013487ed263f970c01538e5a02c1970b.jpg" title="Figure2" /></a>&#0160;<br /><strong>Figure 2</strong></p>
<ul>
<li>Since there were still two FCoE Adapter instances, I still had two unique WWPNs and as a result, there was no impact to Fabric zoning.</li>
<li>Another interesting point was that when I created the vFC on the 5548s, I had to bind them to the virtual port channel.&#0160; While this worked fine when connecting to two different 5548s, if you connect both CNAs to the same 5548 and attempt to do the same thing, it will not work properly and only one of the CNAs will be allowed to complete FCoE login by the switch.&#0160; I don’t view this as a problem and believe everything is working as designed.&#0160; The only reason I did it this way was to troubleshoot a vPC issue and wanted to remove the second vPC chassis from the configuration.&#0160; I ended up making the configuration so simple that it actually didn’t make sense anymore.&#0160; Sort of like trying to troubleshoot a LAG related problem with only one link…</li>
<li>For testing purposes, we ran block I/O over FCoE and file I/O (CIFS) simultaneously and then performed some cable pull testing to ensure that failover and failback would work properly.&#0160; I was happy to observe that for both block and file I/O it worked very well.&#0160; </li>
</ul>
<p>For more information on configuring vPC with FCoE, see <a href="http://www.emc.com/collateral/hardware/technical-documentation/h6290-fibre-channel-over-ethernet-techbook.pdf" target="_self">the FCoE TechBook</a>.</p>
<p>The downside to this configuration is that it requires a bunch of additional administration steps and in my experience it makes troubleshooting a bit more complex.&#0160; However, if you need to use active/active teaming in your converged network, the additional complexity may be worth the extra work.&#0160;</p>
<p>An interesting development with this type of configuration, recently released by Brocade, is Virtual Cluster Switching or VCS.&#0160; VCS will eventually allow for the topology like the one shown in figure 1 but it will mostly self configure and this will drastically reduce the administrative burden of creating such a topology.&#0160; EMC is currently working with the VDX switch / VCS feature and should be announcing a supported topology sometime in the near future.</p>
<p><strong>Adjusting the “Air-gap” requirement</strong></p>
<p>Since the topology shown in figure 1 allows a host to connect to <strong>physically separate</strong> switches and for the FC fabrics to remain <strong>logically isolated</strong>, I don’t believe the SAN A / SAN B principle is being violated.&#0160; As a result, I don’t believe an adjustment to the SAN A / SAN B best practice is required.&#0160; Rather, I think we need to consider a redundant fabric topology in which some of the switches are logically joined by a separate protocol such as vPC or VCS, as a valid redundant fabric topology that can be used in a converged network environment.&#0160; That having been said, I’d like to hear your thoughts…</p>
<p><strong>For more information…</strong></p>
<p>As I mentioned in a <a href="/brasstacks/conversation-topics-for-emc-world-2011/" target="_self">previous post</a>, I’ll be presenting at <a href="http://www.emcworld.com/" target="_self">EMC World</a> this year. &#0160;My presentation was originally going to be an updated version of last year’s but I ended up almost completely re-writing the entire slide deck.&#0160; This year I’ll be talking about:</p>
<ul>
<li>the “Air-gap fabric” requirement</li>
<li>the updates to our supported topologies</li>
<li>the impact the release of FCoE on director class products and the introduction of VE_Ports have had on the supported topologies</li>
<li>three “real world” converged network use cases.&#0160; One of the converged network examples will cost almost 60% less than the non-converged reference topology I’ll be providing and use only 60% of the power!</li>
</ul>
<p>If you’re interested in attending, I’ll be presenting on Tuesday from 5:00 to 6:00 and on Wednesday from 4:15-5:15.&#0160; Also, there will be a Future of Storage Networking “Birds of a Feather” session on Wednesday morning from 8:30 – 9:30.</p>
<p>Hope to see you there!</p>
<p>Thanks for reading!</p>
