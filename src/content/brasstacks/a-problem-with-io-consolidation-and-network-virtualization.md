---
title: "A problem with I/O Consolidation… and Network Virtualization?"
pubDate: 2012-09-05
postedAt: "01:33 PM"
description: "Some number of weeks ago I helped troubleshoot an FCoE problem involving a flaky twinax cable that was causing excessive bit errors. The symptom being observed was very strange at first glance; CRC errors were being logged on interfaces that should have been idle. At first we thought the switch..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2012/09/a-problem-with-io-consolidation-and-network-virtualization.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250913093418/https://brasstacksblog.typepad.com/brass-tacks/2012/09/a-problem-with-io-consolidation-and-network-virtualization.html"
pdf: "/brasstacks/a-problem-with-io-consolidation-and-network-virtualization/a-problem-with-io-consolidation-and-network-virtualization.pdf"
comments:
  - author: "Ivan Pepelnjak"
    date: "09/05/2012 at 02:43 PM"
    html: |-
      <p>I would love to know which switch you were using. In the good old days a switch (OK, maybe it was called a bridge then) would drop a frame with a CRC error, not forward it. </p>
      <p>There should be no transmit CRC errors in a store-and-forward switch. Cut-through switches are a different story. They were a bad idea in 1990&#39;s and they still are.</p>
  - author: "Dmitri Kalintsev"
    date: "09/05/2012 at 11:20 PM"
    html: |-
      <p>Hi Eric,</p>
      <p>Cut-through switching is extremely uncommon in data networking, or at least it was until recently. Now that you mentioned it, I&#39;m very interested in checking with the modern Ethernet &quot;kings of low latency&quot; to see if they are using cut-throgh.</p>
      <p>IMO, it is bad idea; I&#39;m very much with Ivan on this one.</p>
  - author: "Waldemar Pera"
    date: "09/06/2012 at 07:01 AM"
    html: |-
      <p>Great post! It&#39;s a very interesting trouble and a good opportunity to remember what happened &quot;under the hood&quot;.</p>
  - author: "Erik"
    date: "09/06/2012 at 08:31 AM"
    html: |-
      <p>Hi Ivan, in this case I’m hoping to avoid naming a specific FCoE switch vendor or product.  That having been said, I believe that Brocade, Cisco and Juniper FCoE switches will all exhibit this symptom.  I’m only naming these three because they are the only FCoE switches that I have direct experience with.<br />
      <br />
      In regards to NV and whether or not the switches that will be used in the underlay will use cut-through or store and forward.  I’ve noticed that most of the 10GbE ToR switches I’ve been looking at recently are all claiming latencies of less than 1 usec.  To me this indicates they must be using cut-through because it will take at least 1.2 usec to receive 1500 Bytes when using 10GbE (12375 encoded bits / signaling rate of 10.3125 Gbps )<br />
      </p>
  - author: "Erik"
    date: "09/06/2012 at 08:34 AM"
    html: |-
      <p>Hi Dkalintsev, I think it&#39;s becoming much more common especially since switch vendors appear to be using the latency metric as a way to differentiate themselves from their competition.</p>
  - author: "Erik"
    date: "09/06/2012 at 08:35 AM"
    html: |-
      <p>Thanks Waldemar!</p>
  - author: "Brook Reams"
    date: "09/06/2012 at 10:25 AM"
    html: |-
      <p>Erik,</p>
      <p>It seems that part of the reason for the bad behavior is because Ethernet relies on frame flooding to determine an unknown address. </p>
      <p>In the case of Fiber Channel, since devices login and register with a name service, finding an unknown address does not rely on frame flooding. </p>
      <p>As you point our, cut through switching becomes mandatory as link rates go up so the original store and forward architecture isn&#39;t feasible and the CRC can only be acted upon by the edge device at the destination. </p>
      <p>A tentative conclusion open for debate follows:<br />
      1. Finding an unknown destination should rely on a name service and device registration when cut and forward switching is prevalent.</p>
      <p>BTW, very useful post with great detail.<br />
      </p>
  - author: "Erik"
    date: "09/06/2012 at 03:07 PM"
    html: |-
      <p>Hi Brook, thanks!  </p>
      <p>Not using cut-through with OVNs would potentially solve the problem but could create others.</p>
      <p>Another idea would be to add a checksum to the &quot;TNID&quot; field and specify that the Tunnel End Points validate and then discard if the validation fails.  Not sure how realistic this is though..</p>
  - author: "Dmitri Kalintsev"
    date: "09/06/2012 at 06:39 PM"
    html: |-
      <p>Hi Eric,</p>
      <p>I followed up with one of my vendor friends, who confirmed that their low latency data-only gear also operates in cut-through mode. His recommendation was that the Layer 1 errors are to be closely and pro-actively monitored, and identified bad talkers acted upon as soon as possible. Some network devices can trigger port actions (such as shut) based on error thresholds, based for e.g. on CRCs, but whether to use this or not would depend on the particular environment, of course.</p>
      <p>I agree with the recommendation to monitor and quick act on errors; and it should work equally well with NV.</p>
      <p>Cheers,</p>
      <p>-- Dmitri</p>
  - author: "Krunal"
    date: "09/06/2012 at 10:44 PM"
    html: |-
      <p>This is common problem with any cut thru switching. Nexus 5500 introduces a feature called stomping in which switch does bit flapping in a CRC portion of the ethernet frame.<br />
      9000 byte frame with bit flaps/ bad CRC arrives to the switch port 1.<br />
      After first 64 bytes received switch decides to send to port 2 and port starts receiving the full frame and putting on wire.</p>
      <p>Now last 4 bytes of frame received on ingress port and switch finds that oh this is bad frame but you cannot pull bits from wire. So switch does bit flapping on the CRC and continues to forward the frame however, it accounts on interface counter RX CRC on ingress port and output error on egress port. </p>
      <p>If next switch is stored and forward this bad CRC frame will be dropped on ingress port. </p>
      <p>If next switch is cut thru that switch does the same process. </p>
      <p>All above does not prevent switch from making wrong switching decision because of bit flap in DST_MAC or ether type. But bad CRC frames are identified by next switch. </p>
  - author: "Erik"
    date: "09/07/2012 at 08:46 AM"
    html: |-
      <p>Hi Krunal, I agree with what you are saying and have observed this behavior in the lab as well.  </p>
      <p>What do you think about adding a checksum that will cover the VNID field?</p>
  - author: "Erik"
    date: "09/07/2012 at 08:53 AM"
    html: |-
      <p>Dmitri, thanks for the confirmation.  Perhaps the answer is as simple as monitor for bit errors or set an aggressive policy that would force an interface offline after exceeding a certain bit error rate..</p>
      <p>That having been said, I was hoping for something a bit more automated and was thinking that by adding some kind of checksum to the encap header, that the networking gear could take care these situations automatically (like store and forward architectures do).     </p>
  - author: "Krunal"
    date: "09/07/2012 at 09:20 AM"
    html: |-
      <p>I dnt know but as you might be already be aware checksum also cannot detect full error. We have checksum filed for each IP header and Not all routers calculates checksum for all IP packets passed thru it. This is one reason IPv6 header is not protected by a checksum. </p>
  - author: "Dmitri Kalintsev"
    date: "09/07/2012 at 07:45 PM"
    html: |-
      <p>Eric,</p>
      <p>I guess the &quot;correct&quot; answer is, as always, &quot;it depends&quot;. In some environments it may be better to drop the defective frames and try to carry on, while in others it could make much better sense to cut off the offender as soon as possible.</p>
      <p>My &quot;gut feel&quot; preference is clearly on the side of isolating and fixing the root cause as soon as possible (because even if you carry on, you still know that you&#39;ll need an outage to fix the problematic hardware), but on the other hand if bad frames were dropped (meaning their impact is isolated to the directly affected system/s), and their volume wasn&#39;t very high, there would be more operational flexibility in regards to when to do the repairs in a more planned manner.</p>
      <p>As I said, &quot;it depends&quot;. :)</p>
      <p>Regarding the idea of introducing an additional CRC for headers - I&#39;m quite sceptical, as in addition to changes to networking standards it would almost certainly require changes to the networking hardware.</p>
      <p>Cheers,</p>
      <p>-- Dmitri</p>
  - author: "dort"
    date: "09/19/2012 at 01:02 AM"
    html: |-
      <p>I was able to find good information from your articles.</p>
  - author: "Erik"
    date: "09/25/2012 at 10:31 AM"
    html: |-
      <p>Thanks Dort.</p>
  - author: "Will Hogan"
    date: "11/08/2012 at 08:33 AM"
    html: |-
      <p>Erik,</p>
      <p>This was a great post and I learned a lot.  Thanks a lot!</p>
  - author: "Erik"
    date: "11/09/2012 at 08:06 AM"
    html: |-
      <p>Hi Will, I&#39;m glad you found it useful!  Thanks for taking the time to comment.</p>
      <p>Erik </p>
  - author: "Erwin van Londen"
    date: "11/19/2012 at 12:56 AM"
    html: |-
      <p>Hi Erik,</p>
      <p>Good post and great find. It&#39;s always a PITA to find these kind of issues without an analyzer. </p>
      <p>In FC we don&#39;t have &quot;VLAN/VSAN flooding&quot;. If an in-frame error is encountered whereby the CRC is incorrect and cut-through switching is used (as all FC switches do these days) we simply terminate the frame with EOFti where we invalidate the frame. We do not drop the frame on the next ingress port but we let the recipient handle this. This does prevent additional overhead on the all the ASIC&#39;s and is the fastest way of handling these kind of errors. </p>
      <p>As for discussing whether cut-trough routing/switching is better or worse then store&amp;forward is up for grabs. There are pros&amp;cons to both.</p>
      <p>Cheers,<br />
      Erwin</p>
  - author: "Erik Smith"
    date: "11/24/2012 at 06:45 PM"
    html: |-
      <p>Hi Erwin, thanks!  I agree with your description of how this is handled with FC.</p>
  - author: "Bill Hubert"
    date: "03/06/2013 at 01:20 AM"
    html: |-
      <p>Your post was very informative thank you for that</p>
  - author: "Erik"
    date: "03/29/2013 at 08:17 AM"
    html: |-
      <p>Thanks Bill!   </p>
---

<p>Some number of weeks ago I helped troubleshoot an FCoE problem involving a flaky twinax cable that was causing excessive bit errors.&#0160; The symptom being observed was very strange at first glance; CRC errors were being logged on interfaces that should have been idle.&#0160; At first we thought the switch was simply incrementing the wrong CRC counter, but as we would soon discover, the root cause was much more interesting.&#0160; In addition, after reviewing the NVGRE, VXLAN and STT encapsulation proposals, I believe a similar sort of problem may exist with all three proposals.&#0160; If this turns out to be the case, I think now would be the time to address it.</p>
<p>The problematic FCoE topology was similar to the following:</p>
<p><a class="asset-img-link" href="/brasstacks/a-problem-with-io-consolidation-and-network-virtualization/6a013487ed263f970c017c31aac4e9970b.jpg" style="display: inline;"><img alt="One" border="0" class="asset  asset-image at-xid-6a013487ed263f970c017c31aac4e9970b image-full" src="/brasstacks/a-problem-with-io-consolidation-and-network-virtualization/6a013487ed263f970c017c31aac4e9970b.jpg" title="One" /></a></p>
<p>As shown in the above diagram, the defective twinax cable was used to connect Server 1 to interface 1 on the FCoE switch.&#0160; Since we were performing FCoE I/O between Server 1 and the Storage, and we knew the twinax cable was causing bit errors, we expected to see:</p>
<ol>
<li>the “receive CRC error” counter increment on FCoE switch interface 1, </li>
<li>the “transmit CRC error” counter increment on FCoE switch interface 3; and </li>
<li>the “receive CRC error” counter increment on the storage array.</li>
</ol>
<p>Unfortunately, this wasn’t the case and instead we observed:</p>
<ol>
<li>the expected behavior from above; AND</li>
<li>the “transmit CRC error” counter occasionally increment on FCoE switch interface 2!&#0160; This was completely unexpected because only Server 1 was generating any kind of significant I/O and it was all FCoE based.&#0160; Therefore this traffic should only have been visible to the storage array and Server 2 should not have been receiving any frames.&#0160;&#0160;&#0160;</li>
</ol>
<p>Upon reviewing an xgig trace between FCoE switch interface 3 and the storage port, I noticed not only a few CRC errors, but I also noticed a number of ABTS and bad SCSI status frames.&#0160; As I expected, these were related to an exchange or I/O that was impacted by a corrupted frame.&#0160; However, in at least one of the cases, the bad SCSI status was being returned by the Storage port when it detected a missing frame.&#0160; The significance of this wouldn’t be clear until later.&#0160; </p>
<p>Finally we inserted the analyzer between between Server 2 and FCoE Switch interface 2.&#0160; We set it to trigger on bad CRC/FCS and when it triggered I was very surprised to see an FCoE data frame from Server 1 that was addressed to D_ID of the storage array!&#0160; I mean think about this for a second, a frame containing data sent from a host to the storage array was being transmitted to another host on a completely different VLAN!</p>
<p>The reason this happened has to do with one of the basic mechanisms of Ethernet switching known as the unicast flood.&#0160; In a previous post, I described the process of forwarding in an FCoE environment, so rather than rehash that here, I’ll direct those of you who want more detail to <a href="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-2-fip-snooping-bridges-and-fibre-channel-forwarders/" target="_self">that post</a>.&#0160; In this case, the FCoE frame was being flooded because the corruption occurred in Ethertype field.</p>
<p>For additional detail, refer to the diagram of a typical FCoE Frame below.&#0160; Note that with FCoE, the frame typically starts with the Ethernet DA and SA and then is followed by the 802.1Q VLAN Tag.&#0160; </p>
<p><a class="asset-img-link" href="/brasstacks/a-problem-with-io-consolidation-and-network-virtualization/6a013487ed263f970c017c31aac6cf970b.jpg" style="display: inline;"><img alt="Two" border="0" class="asset  asset-image at-xid-6a013487ed263f970c017c31aac6cf970b image-full" src="/brasstacks/a-problem-with-io-consolidation-and-network-virtualization/6a013487ed263f970c017c31aac6cf970b.jpg" title="Two" /></a></p>
<p>In general, when an Ethernet frame is received with a VLAN tag, if the DA is known, the frame will be forwarded based upon a MAC Address table that reflects the switches understanding of the correct route to the destination address.&#0160; If the DA is unknown, the frame will be flooded on that VLAN and eventually the MAC Address table will be updated to allow future frames to be forwarded to the appropriate destination.&#0160; Taking this a step further, if the frame is a FIP or FCoE frame, additional forwarding rules will be applied that are (hopefully) consistent with FC-BB-5 annex C and D.&#0160; These additional rules are described in another post that has to do with <a href="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/" target="_self">FIP Snooping Bridges</a>.&#0160; </p>
<p>Three additional items that I have to mention before getting to the point:</p>
<ol>
<li>the 802.1Q tag is actually an Ethertype (0x8100) that allows the switch to interpret the rest of the frame&#0160; (e.g., VLAN ID) and then actual Ethertype of the frame (e.g., FCoE or 0x8906).</li>
<li>The FCoE capable switches that I am aware of do not learn Fabric Provided MAC Addresses (FPMAs) in the same way that normal MAC Addresses are learned.&#0160; Part of the reason has to do with the special handling requirements outlined above.</li>
<li>Due to performance concerns, the FCoE capable switches that I am aware of all support cut-through routing of FCoE frames, this means that the frame header can be transmitted before the FCS is received.&#0160; As a result, frames with bad FCS are forwarded..&#0160;&#0160;&#0160;</li>
</ol>
<p>Getting back to the trace between FCoE Switch interface 2 and server 2; in the trace I captured, I noticed that the frame with a bad FCS had a VLAN Tag that was incorrect (let’s say 8101, to be honest I can’t remember the exact value).&#0160; As a result, instead of the switch detecting an Ethertype of 0x8100 and handling it appropriately, it detected a different Ethertype (0x8101) and did what any Ethernet switch would do when a frame is received on the default VLAN (remember, no VLAN ID since the tag was corrupted) and the DA is unknown (due to the FPMA learning restriction) and this is to flood it on the default VLAN.</p>
<p>To make matters more interesting, in order for FIP to work properly, a default VLAN must be defined and typically all FCoE devices will use the same default VLAN for FIP VLAN discovery.&#0160; Note, this isn’t a requirement of the protocol, but it is easiest to configure it this way and it works perfectly fine as long as there are no bit errors.&#0160;</p>
<p>The bottom line is this; if you are using FCoE and you are experiencing bit errors, there is a chance (albeit a small one) that an FCoE data frame may be flooded on the default VLAN and this VLAN will probably be used by other FCoE capable devices.&#0160; As a result, ensuring that there are no bit errors logging in your FCoE environment is a VERY good idea.&#0160; </p>
<p>Does this mean you should avoid FCoE?&#0160; Of course not!&#0160; The same problem can occur in any Ethernet network (as long as cut-through routing is used).&#0160; I’ll go out on a limb and say that this problem could occur any time protocol based isolation is used to partition a physical link.&#0160; Note that I explicitly said PROTOCOL based, I am not asserting that this could happen with DWDM or TDM based approaches.</p>
<p><strong>The implications to Network Virtualization</strong></p>
<p>Network Virtualization supports multi-tenancy and the current approaches use a protocol based partitioning method.&#0160; Essentially, all of the proposed tunneling encapsulations (e.g., VXLAN, NVGRE and STT) make use of a “Tenant ID” to signal to the tunnel end points which tenant the frame belongs to.&#0160; Although I have not had the opportunity to force a similar type of problem to occur with any of the proposed NV approaches, I think it may be possible for a bit in the Tenant ID field to get flipped and for a data frame to be delivered to the wrong Tenant. In fairness, this problem would seem to be much less likely to happen with NV and could probably be prevented from occurring by the NV Control Plane.&#0160; As a result, I’ll avoid speculating much more on what could happen until I have more data.&#0160; That having been said, I’m raising the issue now so that it can be investigated by those of us who are interested and a solution can be built in to the protocols (if needed).&#0160; </p>
<p>Thanks for reading! </p>
