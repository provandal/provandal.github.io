---
title: "NVMe over Fabrics: Not ready (yet)"
pubDate: 2017-07-24
postedAt: "10:47 AM"
description: "Image credit: https://www.someecards.com/usercards/viewcard/MjAxMy03ZWMxZjIxZmRkMjRmZGNl/ If you’re into IT infrastructure and you aren’t yet familiar with NVMe and its potential benefits, now would probably be a good time to start reading. In fact, since there’s already so much high quality material that describes what NVMe is, why it’s useful and how it..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2017/07/nvme-over-fabrics-not-ready-yet.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250910171031/https://brasstacksblog.typepad.com/brass-tacks/2017/07/nvme-over-fabrics-not-ready-yet.html"
pdf: "/brasstacks/nvme-over-fabrics-not-ready-yet/nvme-over-fabrics-not-ready-yet.pdf"
comments:
  - author: "Brett"
    date: "08/01/2017 at 06:48 PM"
    html: |-
      <p>Fantastic blog entry as always, Erik.  Can you provide any update to the status of TDZ?  Is Dell/EMC, Cisco, and Brocade going to (or have they already) embrace it for their FC platforms?  When you first blogged about it I got super excited but haven&#39;t seen much about it since.  I&#39;ve been leveraging MDS&#39;s Smart Zoning feature which certainly helps the config process but it&#39;s no TDZ. :-)</p>
  - author: "Erik Smith"
    date: "08/03/2017 at 10:51 AM"
    html: |-
      <p>Hi Brett, thanks!</p>
      <p>With regards to TDZ.  August 6th will mark the 10th anniversary of the day I came up with the idea.  Since then, despite beating every bush and using every approach I could think of, the sad fact is none of the Dell EMC storage platforms support the feature (today).   </p>
      <p>That said Brocade has supported it since FOS 8.0.  </p>
      <p>Also, I&#39;m watching (with a perverse sense of amusement) the stuff the HPE is doing with SmartSAN (which they&#39;ve referred to as Target Driven Peer Zoning).  It&#39;s just nice to know that the idea went somewhere... :-)</p>
      <p>I&#39;ve also heard of a couple of other Flash array vendors that support it but I haven&#39;t dug into it much.</p>
      <p>I agree Smart Zoning isn&#39;t TDZ but it seems to be a step in the right direction and it is available today!</p>
      <p>I will post the mother of all blog posts the day that Dell EMC supports the feature, which I still hope will happen at some point.  </p>
      <p>Regards, Erik    </p>
---

<p style="text-align: center;"><a class="asset-img-link" href="/brasstacks/nvme-over-fabrics-not-ready-yet/6a013487ed263f970c01bb09b1eab0970d.png" style="display: inline;"><img alt="WatchedPot" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb09b1eab0970d img-responsive" src="/brasstacks/nvme-over-fabrics-not-ready-yet/6a013487ed263f970c01bb09b1eab0970d.png" title="WatchedPot" /></a></p>
<p style="text-align: center;"><span style="font-size: 8pt;">Image credit: https://www.someecards.com/usercards/viewcard/MjAxMy03ZWMxZjIxZmRkMjRmZGNl/</span></p>
<p>If you’re into IT infrastructure and you aren’t yet familiar with NVMe and its potential benefits, now would probably be a good time to start reading.&#0160; In fact, since there’s already so much <a href="https://jmetz.com/2016/08/a-nvme-bibliography/">high quality material</a> that describes what NVMe is, why it’s useful and how it works, I’m not going to go into those details here.&#0160;</p>
<p>This post is also not going to focus directly on NVMe over Fabrics.&#0160; The reason is, based on our limited testing, from a system level point of view I think it’s too early to say much about it.&#0160; I will say many of the features that our customers would expect from an enterprise class storage protocol simply haven’t been created for NVMe over Fabrics yet.&#0160; As I’ll describe below, we’ve found that the missing functionality varies based on the transport being used.&#0160; For example, in the case of RoCE and iWARP they need to do a bit of work on “Discovery”.&#0160; With regards to Fibre Channel, it comes down to the lack of a GA quality NVMe over Fabrics driver for any of the Tier 1 Operating Systems.&#0160;</p>
<p>In an attempt to be fair to the people currently working to address these limitations, I’ll say I fully expect the majority of these issues to be addressed by sometime in 2018.&#0160;&#0160;&#0160;</p>
<h2>This post will focus on fabrics.&#0160;</h2>
<p>More specifically, the fabrics that are capable of transporting NVMe.&#0160; I’ll also spend some time describing:</p>
<ol>
<li>Why these fabrics aren’t ready for the Enterprise; and</li>
<li>why we’re watching them soooo closely.</li>
</ol>
<p>As shown in the following diagram, these fabrics can be based on RDMA, Fibre Channel or TCP (TCP is pre-standard at this point, although apparently there’s a <a href="https://www.linkedin.com/feed/update/urn:li:activity:6293565279725199360/">demo at the Flash Summit</a>) and use IB, RoCE, iWARP, TCP or Fibre Channel (FC) as transports.&#0160;</p>
<p><a class="asset-img-link" href="/brasstacks/nvme-over-fabrics-not-ready-yet/6a013487ed263f970c01b8d298fb54970c.jpg" style="display: inline;"><img alt="ProtocolStacks3" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b8d298fb54970c image-full img-responsive" src="/brasstacks/nvme-over-fabrics-not-ready-yet/6a013487ed263f970c01b8d298fb54970c.jpg" title="ProtocolStacks3" /></a></p>
<p>For the sake of this blog post, I’m going to focus on the three transports that my team and I feel are the most likely to be used in by our customers and have consequently been working on over the past several years; RoCE, iWARP and FC.&#0160;</p>
<h2>iWARP</h2>
<p>When we first started working with RDMA, I thought iWARP was going to win the protocol war that was going on between it and RoCE.&#0160; My reasoning was very simple, iWARP doesn’t require anywhere near the amount of network configuration that RoCE does (much more on this in the next section) and it isn’t susceptible to congestion spreading (A.K.A., Slow Drain) like all lossless protocols (e.g., RoCE, FC) are.&#0160; In addition, some of the early work we did to compare the performance attributes of RoCE to iWARP showed that they were comparable.&#0160; For example, the chart below was generated from data collected by two Engineers on my team (Alan Rajapa and Massarrah Tannous) during some testing that they performed to compare different implementations of the two transports.&#0160;</p>
<p><a class="asset-img-link" href="/brasstacks/nvme-over-fabrics-not-ready-yet/6a013487ed263f970c01b8d298fb76970c.jpg" style="display: inline;"><img alt="RoCEversusiWARP_v2" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b8d298fb76970c image-full img-responsive" src="/brasstacks/nvme-over-fabrics-not-ready-yet/6a013487ed263f970c01b8d298fb76970c.jpg" title="RoCEversusiWARP_v2" /></a></p>
<p>When reviewing this chart, please keep in mind the following:</p>
<ol>
<li>The chart was created about 18 months ago and represents a point in time when iWARP latency (with a 4.x Linux Kernel) was slightly less (under ideal conditions) than RoCE, and MUCH less than RoCE when any kind of packet loss was introduced.</li>
<li>Some in the RoCE community will complain that this isn’t a fair comparison since RoCE requires a lossless network. My response to this concern has always been “We’re interested in how the protocols react under packet loss conditions because configuring lossless behavior across a L3 Clos (leaf/spine) network is fairly complex and is not something that we (at the time), nor our Customers, have much experience with.&#0160; As a result, we believe lossless (DCB) will be frequently misconfigured and many of our customers may inadvertently end up running RoCE on a lossy network.”&#0160; With this in mind, the purpose of our test was to find out just how screwed our customers would be in this kind of a mis-configuration.&#0160; If RoCE flat out wouldn’t work, these types of situations would be fairly easy to identify and then resolve.&#0160; However, if this kind of mis-configuration resulted in a situation where things mostly worked and just sort of limped along, our support organizations would have a MUCH harder time troubleshooting and this was causing us great anxiety.</li>
<li>Over the past 18 months the RoCE community (Mellanox in particular) has done a <a href="http://www.mellanox.com/blog/2016/07/resilient-roce-relaxes-rdma-requirements/">ton of great work</a> to address many of the issues we’ve raised with regards to packet loss. More on this in the next section.</li>
</ol>
<p>With regards to iWARP going forward, the primary proponent of the protocol appears appears to have found <a href="http://service.chelsio.com/opt-in-out/newsletters/Mar2017/20170326_Chelsio_now_Microsoft_Azure_Stack_Certified.htm">some use cases</a> for it.&#0160; That said, they are really the only vendor pushing it and based on what I’ve heard from others in the industry as well as what our Customers are asking for, my personal opinion is that iWARP will not be the dominant Ethernet based transport for NVMe.&#0160; As a result, I won’t spend any additional time on it here.</p>
<h2>RoCE</h2>
<p>RoCE (RDMA over Converged Ethernet) is an interesting transport for a number of reasons:</p>
<ol>
<li>Due to the need to configure DCB across an L3 network (when running at scale), it is much more complex to configure than FCoE (more on this below).</li>
<li>Since it requires DCB (which includes Priority Flow Control) it’s susceptible to <a href="/brasstacks/slow-drains-are-impacting-your-san/">Congestion Spreading (a.k.a., Slow Drain)</a>. A partial solution to this problem is to use ECN/RED (as described in the Azure/Sigcomm white paper that I linked to below).&#0160; However, this does not address all potential causes of congestion spreading (especially the acute cases).&#0160;</li>
<li>The NICs and the switches that are typically used to transport RoCE lack even the most basic counters to help troubleshoot congestion spreading events (i.e., something analogous to FC’s “<a href="https://web.archive.org/web/20250910171031/https://brasstacksblog.typepad.com/brass-tacks/">time spent at zero transmit credit</a>” counter is needed).</li>
</ol>
<p>Yet despite these limitations, there is more interest in RoCE than iWARP (see Google trends below) and I’m also hearing that it’s much more popular in production environments as well.&#0160; For example, RoCE is being used in production by Azure as <a href="http://conferences.sigcomm.org/sigcomm/2015/pdf/papers/p523.pdf">described in this white paper</a>.&#0160; BTW, I LOVE this white paper because it not only confirms that it’s possible to use RoCE at scale, it also confirms the level of complexity required to properly configure it to avoid issues with congestion spreading.&#0160;</p>
<p><a class="asset-img-link" href="/brasstacks/nvme-over-fabrics-not-ready-yet/6a013487ed263f970c01b7c90eaeb6970b.jpg" style="display: inline;"><img alt="RoCEversusiWARP" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b7c90eaeb6970b image-full img-responsive" src="/brasstacks/nvme-over-fabrics-not-ready-yet/6a013487ed263f970c01b7c90eaeb6970b.jpg" title="RoCEversusiWARP" /></a></p>
<p>A few more points before I go on:</p>
<ol>
<li>For the sake of this blog post, I’m going to focus only on the configuration complexity portion of RoCE.</li>
<li>This complexity is not specific to any one vendor but the following steps are specific to the switch vendor we were testing with at the time.</li>
<li>ECN/RED is being used for congestion avoidance.</li>
<li>In the example below we configure 3 Classes of service (0, 3 and 6) and only really 3 and 6 are required for RoCE and ECN.</li>
<li>A number of vendors have done a ton of work to automate these configuration steps and seem to be heading down the right track towards providing a complete end-to-end configuration tool. &#0160;A notable example is <a href="http://www.mellanox.com/page/products_dyn?product_family=220&amp;mtag=mellanox_neo">Neo</a>&#0160;which Mellanox provided to us a no cost for evaluation purposes.</li>
</ol>
<p>The actual topology that we used for testing RoCE is shown below.</p>
<p>It consists of a spine, two leaf switches, two “Compute” nodes and two “Storage” nodes.&#0160;</p>
<p><a class="asset-img-link" href="/brasstacks/nvme-over-fabrics-not-ready-yet/6a013487ed263f970c01bb09b1eb3b970d.jpg" style="display: inline;"><img alt="TestTopo" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb09b1eb3b970d image-full img-responsive" height="442" src="/brasstacks/nvme-over-fabrics-not-ready-yet/6a013487ed263f970c01bb09b1eb3b970d.jpg" title="TestTopo" width="606" /></a></p>
<p>A summary of the configuration steps that we performed to configure this topology is shown below.&#0160;</p>
<h4>Spine 1: MAC = AA</h4>
<ol>
<li>Configure buffer pools:</li>
<li>Configure Trust level per port:</li>
<li>Map DSCP levels to switch-priority</li>
<li>Map switch-priority to priority-groups</li>
<li>Map ingress priority group traffic to pools.</li>
<li>Map egress traffic class to pools</li>
<li>Map switch-priority to traffic class</li>
<li>Configure the scheduler</li>
<li>Set ECN/RED on the switch.</li>
<li>Enable PFC on the switch
<ol>
<li>Make sure Flow Control is disabled</li>
<li>Make sure Priority Flow Control is enabled</li>
</ol>
</li>
</ol>
<p><strong>&#0160;</strong></p>
<h4>Leaf: MAC = DD and EE</h4>
<ol>
<li>Configure buffer pools:</li>
<li>Configure Trust level per port:</li>
<li>Map DSCP levels to switch-priority</li>
<li>Map switch-priority to priority-groups</li>
<li>Map ingress priority group traffic to pools.</li>
<li>Map egress traffic class to pools</li>
<li>Map switch-priority to traffic class</li>
<li>Configure the scheduler</li>
<li>Set ECN/RED on the switch.</li>
<li>Enable PFC on the switch
<ol>
<li>Create a VLAN, set the end-station facing ports as switchports in trunk mode.</li>
<li>Make sure Flow Control is disabled</li>
<li>Make sure Priority Flow Control is enabled</li>
</ol>
</li>
</ol>
<h2>Fibre Channel</h2>
<p>Disclaimer: I’ve spent the past 20 years working as a member of Dell EMC’s Connectrix Business Unit and my livelihood is pretty much tied directly to FC’s success.&#0160; That said, I suspect you may be surprised to learn that until recently I’ve struggled with the idea of using FC as a transport for NVMe.&#0160;</p>
<p>When I first started reading about NVMe over Fabrics, one of the things that caught my eye was the need for a Discovery Service.&#0160; After a little bit of digging, I realized that most of what NVME over Fabrics needed for discovery could be provided by the FC Name Server and that this fact actually gave the FC transport a slight competitive advantage over the RDMA based transports.&#0160; BTW, this is really just another way of saying FC uses a <a href="/brasstacks/fc-and-fcoe-versus-iscsi-network-centric-versus-end-node-centric-provisioning/">network centric discovery</a> approach and RoCE/iWARP/TCP use an <a href="/brasstacks/fc-and-fcoe-versus-iscsi-network-centric-versus-end-node-centric-provisioning/">end node centric</a> approach.</p>
<p><a class="asset-img-link" href="/brasstacks/nvme-over-fabrics-not-ready-yet/6a013487ed263f970c01bb09b1eb51970d.jpg" style="display: inline;"><img alt="DiscoveryLayers" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb09b1eb51970d image-full img-responsive" src="/brasstacks/nvme-over-fabrics-not-ready-yet/6a013487ed263f970c01bb09b1eb51970d.jpg" title="DiscoveryLayers" /></a></p>
<p>The diagram above illustrates the gap in functionality.&#0160; Just as with SCSI and FCP, there are actually two different kinds of discovery that need to be performed, each operating at different layers in the stack.</p>
<p>The first kind of discovery is Transport specific.&#0160; This discovery process allows two or more ports to discover each other over a network.&#0160; With FC, the endpoints (i.e., VN_Ports) discover each other automatically via the use of the FC Name Server.&#0160; With IP, there is no centralized in-band way to do this short of relying on iSNS (which they shouldn’t).&#0160; To get around this limitation, end users will basically need to do what they do today with iSCSI; individually configure each host to point at the correct targets.&#0160;&#0160;&#0160;</p>
<p>The second kind of discovery is done at the NVMe layer and is fairly well-defined by the <a href="http://www.nvmexpress.org/">NVMe standard</a>.&#0160; This isn’t to say the NVME discovery mechanism is perfect, but it is common across FC, RDMA and TCP transports, and as a result it doesn’t make sense to use it to compare the benefits of different transports.</p>
<p>In terms of configuration complexity, a FC fabric can basically self-form and it supports lossless behavior out of the box.&#0160; The only additional configuration that is typically done is to zone the host and storage ports together, but this doesn’t necessarily need to be done manually (see <a href="/brasstacks/introducing-target-driven-zoning-tdz/">Introducing Target Driven Zoning</a>).&#0160;</p>
<p>So you may be wondering, outside of easier discovery and less configuration why does using FC as a transport for NVMe make sense?&#0160;</p>
<p>To be completely honest, I didn’t think FC was a good fit! (initially) This is because in the early days all of the practical use cases for it seemed to be focused on platform 3 rather than more traditional enterprise applications.&#0160; This causes a problem for FC because <a href="/brasstacks/fibre-channel-is-better-than-ethernet/">platform 3 is generally hostile to FC and storage arrays in general</a>, consequently I didn’t see a real use case for FC, until recently.</p>
<p>This year at Dell EMC World, we included an NVMe section in our <a href="https://www.google.com/url?sa=t&amp;rct=j&amp;q=&amp;esrc=s&amp;source=web&amp;cd=3&amp;ved=0ahUKEwj3lcrRnpbVAhXFez4KHSdYCj0QFggxMAI&amp;url=https%3A%2F%2Femcworldonline.com%2F2017%2Fconnect%2FfileDownload%2Fsession%2FB2B39180D02654047DE1FF2D77BB0498%2Fstorage25.Connectrix%2520Configuring%2520Your%2520SAN%2520To%2520Support%2520All%2520Flash%2520Arrays.pdf&amp;usg=AFQjCNHquYtyzwjA9pakgx-nITweusE1MA">SAN presentation</a>.&#0160; The key points about NVMe from that presentation can be found on slides 135-137.&#0160; To summarize, NVMe SSDs are first being used in compute and they already provide efficiencies over what can be done with SATA based SSDs today.&#0160; These same efficiencies can be realized on the back end of a storage array and <a href="https://blog.dellemc.com/en-us/nvme-the-yellow-brick-road-to-new-levels-of-performance/">Jeff Boudreau has already indicated</a> he has plans to introduce a standards based NVMe solution soon.&#0160; The next logical evolutionary step (shown on slide 137) would be to allow hosts to access the NVMe drives in an array via NVMe over Fabrics.&#0160;</p>
<p>The reason this fabric should be Fibre Channel for our Enterprise customers is because the vast majority of them (85-90%) currently use FC to access their All Flash Arrays and they do so <a href="/brasstacks/fibre-channel-is-better-than-ethernet/">for good reasons</a>.&#0160; So it only makes sense for them to continue to use the same Transport to access the next generation of ultra-low latency NVMe based SSDs.</p>
<p>However, as I mentioned previously, in order for customers to use NVMe over FC, we need GA quality NVMe over FC drivers.&#0160; And then we have to put these drivers through an extensive qualification process (because data integrity).&#0160; I’m thinking that the soonest this might actually happen would be mid 2018.</p>
<p>**BTW, in case you were wondering, ALL FC switches that you can purchase today support NVMe over Fabrics. &#0160;</p>
<h2>Wrapping up</h2>
<p>So what transport should you use?&#0160; As always, I’ll leave that decision up to you.&#0160; But I will say the problem that keeps me up at night is how to address Congestion Spreading; and whether you choose RoCE or FC, you’ll eventually need to deal with this problem.&#0160; Since the FC community has been dealing with Congestion Spreading for years, have hardware support to help detect it and as shown below are continuing to innovate in this area, I would personally choose FC when it’s ready.&#0160;</p>
<p><a class="asset-img-link" href="/brasstacks/nvme-over-fabrics-not-ready-yet/6a013487ed263f970c01b7c90eaf00970b.jpg" style="display: inline;"><img alt="PicCSPAvoidance" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b7c90eaf00970b image-full img-responsive" src="/brasstacks/nvme-over-fabrics-not-ready-yet/6a013487ed263f970c01b7c90eaf00970b.jpg" title="PicCSPAvoidance" /></a></p>
<p>BTW, “Future Fibre Channel Enhancements (TBD)” is being actively discussed and I hope to be able to share more details about it here at some point in the future.</p>
<p>Thanks for reading!</p>
