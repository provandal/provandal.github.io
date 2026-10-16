---
title: "Slow Drains are impacting your SAN!"
pubDate: 2016-02-02
postedAt: "08:57 AM"
description: "If you work with Fibre Channel on a regular basis and have come to depend on its excellent performance attributes, you might be surprised to learn that many of the cases handled by our SAN team in Customer Support are related to performance problems. Typically, as we dig into these..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2016/02/slow-drains-are-impacting-your-san.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250910160242/https://brasstacksblog.typepad.com/brass-tacks/2016/02/slow-drains-are-impacting-your-san.html"
pdf: "/brasstacks/slow-drains-are-impacting-your-san/slow-drains-are-impacting-your-san.pdf"
comments:
  - author: "Ross Zubritski"
    date: "02/10/2016 at 01:14 PM"
    html: |-
      <p>Great write-up.   Thank you and Howard and Dennis...</p>
      <p>--Ross Z<br />
      </p>
  - author: "Dynamoxxx"
    date: "02/21/2016 at 10:55 PM"
    html: |-
      <p>Very informative. Can&#39;t get to EMC article, says page not found (i am logged-in to support.emc.com)</p>
  - author: "Erik Smith"
    date: "02/23/2016 at 02:00 PM"
    html: |-
      <p>Thanks Dynamox!  I updated the link to reflect the new KB article number.   </p>
  - author: "Dinesh Yadav"
    date: "09/06/2018 at 12:49 AM"
    html: |-
      <p>Nice and very useful post.</p>
---

<p>If you work with Fibre Channel on a regular basis and have come to depend on its excellent performance attributes, you might be surprised to learn that many of the cases handled by our SAN team in Customer Support are related to performance problems.&#0160; Typically, as we dig into these cases, we discover the majority of them are not actually caused by the FC switches themselves, but rather by end devices that are not performing as expected and are causing fabric wide congestion.&#0160; These misbehaving end devices are referred to as “slow drains” and they represent a well-known class of problem that is inherent to all lossless transports including FC, DCB Ethernet (e.g., FCoE, RoCE) and even wastewater drain systems (e.g., “Plumbing”).</p>
<p>For example, let’s assume that we have a pipe that is capable of transporting 16Gps (Gallons per second) but an outlet that only allows 8Gps.&#0160; As long as the amount of water flowing through the pipe is less than or equal to 8Gps, the water will flow out of the pipe at approximately the same rate as it flows into it.&#0160; As you would probably expect, since there is 16Gps of capacity in the pipe, the rate at which water flows into the pipe could exceed 8Gps for short periods of time and the pipe could act as a kind of buffer.&#0160; You would also probably expect that if you were to consistently exceed an average of 8Gps, you would quickly notice the water level in the pipe starting to rise.&#0160;</p>
<p><a class="asset-img-link" href="/brasstacks/slow-drains-are-impacting-your-san/6a013487ed263f970c01b7c8100aa6970b.jpg" style="display: inline;"><img alt="B4one" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b7c8100aa6970b img-responsive" src="/brasstacks/slow-drains-are-impacting-your-san/6a013487ed263f970c01b7c8100aa6970b.jpg" style="display: block; margin-left: auto; margin-right: auto;" title="B4one" /></a></p>
<p>The same sort of problem can happen within a FC SAN for a number of reasons, including:</p>
<ol>
<li>A mismatch between the maximum link speeds supported by the Initiator and the Target</li>
<li>The use of Fan in / Fan out</li>
<li>Using an oversubscribed ISL</li>
<li>An end device not accepting data at the same rate at which it’s arriving (e.g., acting as a slow drain)</li>
</ol>
<p>It’s important to note that in all of the above scenarios, <a href="https://www.emc.com/collateral/hardware/technical-documentation/h4331-networked-storage-cncpts-prtcls-sol-gde.pdf">Buffer-to-Buffer flow control</a> is used to ensure that there is sufficient buffering available on the receiver to store all frames put onto the wire by the transmitter.&#0160; As a result, the transmitter experiences congestion whenever it is unable to transmit a frame due to a lack of buffer at the other end of the link.&#0160; For example, as shown below, congestion has spread from the Target back towards the Initiator due to a mismatch in data rates.</p>
<p><a class="asset-img-link" href="/brasstacks/slow-drains-are-impacting-your-san/6a013487ed263f970c01bb08b4c926970d.jpg" style="display: inline;"><img alt="One" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb08b4c926970d image-full img-responsive" src="/brasstacks/slow-drains-are-impacting-your-san/6a013487ed263f970c01bb08b4c926970d.jpg" title="One" /></a></p>
<p>The impact that the problem being shown above will have on the rest of the fabric might not be obvious at first glance but let’s see what happens with a slightly more complicated topology.&#0160; I’ll start by adding another Initiator and Target pair (e.g., Initiator 2 and Target 2).&#0160; Note that the receive queue on switch A contains 3 frames, one for Target 1 and two for Target 2. &#0160;Since there is ample space in the receive queue on switch A, the Initiators attached to Switch B are probably not experiencing congestion very often.</p>
<p><a class="asset-img-link" href="/brasstacks/slow-drains-are-impacting-your-san/6a013487ed263f970c01bb08b4c939970d.jpg" style="display: inline;"><img alt="Two" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb08b4c939970d image-full img-responsive" src="/brasstacks/slow-drains-are-impacting-your-san/6a013487ed263f970c01bb08b4c939970d.jpg" title="Two" /></a></p>
<p>However, if I slow down the rate at which Target 1 is pulling frames from its queue, you notice that something very interesting happens as shown below.</p>
<p><a class="asset-img-link" href="/brasstacks/slow-drains-are-impacting-your-san/6a013487ed263f970c01bb08b4c941970d.jpg" style="display: inline;"><img alt="Three" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb08b4c941970d image-full img-responsive" src="/brasstacks/slow-drains-are-impacting-your-san/6a013487ed263f970c01bb08b4c941970d.jpg" title="Three" /></a></p>
<p>Note that Target 1 appears to be receiving frames at a rate faster than it can process them and as a result its local queue is filled.&#0160; This in turn causes the receive queue on switch A to fill with frames destined to Target 1 since the frames destined to Target 2 are transmitted soon after they are received.&#0160; In extreme cases, such as the one shown above, this congestion can spread all the way back to the Initiators and prevent them from transmitting frames. &#0160;When things get to this point we typically see two basic scenarios:</p>
<ol>
<li>Target 1 is truly stuck and not releasing ANY credits. &#0160;In this situation, this condition can persist for up to 2 seconds&#0160;at which point the switch will initiate the Link Reset protocol.</li>
<li>Target 1 is not completely stuck, and as illustrated in the first diagram, is instead only capable of processing frames at a rate which is slower than the rate at which they are arriving.&#0160; In this case, the impact to the rest of the environment can be both significant and long lived, at least until the condition is detected and resolved.&#0160; &#0160;&#0160;&#0160;</li>
</ol>
<p>While the above scenarios may seem a bit extreme, they can and do happen in our customer’s environments.&#0160; As you can imagine, when these events occur they can be very painful because they have such a wide impact and can be somewhat hard to troubleshoot.&#0160; In addition, the reason that a particular end-device (both Initiators and Targets) act as a slow drain is not very well understood at this point in time.&#0160; As a result, we decided to come up with a process to help identify, troubleshoot, resolve and prevent slow drain devices; an overview this process can be found in <a href="https://support.emc.com/kb/464027">EMC KB 464027</a> and is shown below for reference.</p>
<p>Our hope is that our customers will use this process to help them detect the presence of potential slow drain devices before they become a significant problem and impact their environments. &#0160;There&#39;s also a ton of background information and links to deep dives on the different concepts involved in case you need it. &#0160;&#0160;&#0160;</p>
<p><a class="asset-img-link" href="/brasstacks/slow-drains-are-impacting-your-san/6a013487ed263f970c01b7c81009e0970b.jpg" style="display: inline;"><img alt="Four" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b7c81009e0970b image-full img-responsive" src="/brasstacks/slow-drains-are-impacting-your-san/6a013487ed263f970c01b7c81009e0970b.jpg" title="Four" /></a></p>
<p>Special thanks to Dennis Makishima and Howard Johnson from Brocade for all of the work they have done to get to the bottom of the slow drain issues being observed and enabling us to start addressing these issues.</p>
<p>Thanks for reading!</p>
<p>Erik</p>
