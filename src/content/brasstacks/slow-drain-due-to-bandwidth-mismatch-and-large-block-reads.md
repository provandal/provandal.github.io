---
title: "Slow Drain due to Bandwidth mismatch and Large Block READs"
pubDate: 2017-04-13
postedAt: "05:27 PM"
description: "Every once in a while, you come across information that makes you understand something in a completely new way. Image credit: https://farscapedevelopment.wordpress.com/2012/07/06/eureka/ I had just such an experience a few weeks back, and Alan Rajapa and I have been working in the lab since then to try and come to..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2017/04/slow-drain-due-to-bandwidth-mismatch-and-large-block-reads.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250911082317/https://brasstacksblog.typepad.com/brass-tacks/2017/04/slow-drain-due-to-bandwidth-mismatch-and-large-block-reads.html"
pdf: "/brasstacks/slow-drain-due-to-bandwidth-mismatch-and-large-block-reads/slow-drain-due-to-bandwidth-mismatch-and-large-block-reads.pdf"
comments: []
---

<p>Every once in a while, you come across information that makes you understand something in a completely new way.</p>
<p><a class="asset-img-link" href="/brasstacks/slow-drain-due-to-bandwidth-mismatch-and-large-block-reads/6a013487ed263f970c01b8d2778b30970c.gif" style="display: inline;"><img alt="Eureka" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b8d2778b30970c img-responsive" src="/brasstacks/slow-drain-due-to-bandwidth-mismatch-and-large-block-reads/6a013487ed263f970c01b8d2778b30970c.gif" title="Eureka" /></a></p>
<p><span style="font-size: 8pt;">Image credit: https://farscapedevelopment.wordpress.com/2012/07/06/eureka/</span></p>
<p>I had just such an experience a few weeks back, and Alan Rajapa and I have been working in the lab since then to try and come to terms with it.</p>
<p>The person who originally provided the test data is a gentleman by the name of Vijay and what he noticed is extremely insightful, relatively easy to understand, and since we’ve confirmed it in the lab, I can now state that I believe:&#0160;&#0160;</p>
<p><strong>Any time an FC HBA or FCoE CNA is performing multiple sequential Large Block READs (&gt; 128k block size) AND the HBA/CNA:Storage bandwidth ratio is less than 1 (e.g., 4G FC HBA and 8G storage, 10G FCoE CNA and 16G storage, etc), the HBA/CNA will start behaving as a <a href="https://support.emc.com/kb/464206">mild slow drain</a>&#0160;and cause <a href="/brasstacks/slow-drains-are-impacting-your-san/">congestion spreading</a>. </strong></p>
<p>We’ve found the above rule holds for all HBA/CNA and OS combinations that we’ve tested.</p>
<p>So you may be wondering why this is important? The answer has to do with the impact that congestion spreading has on innocent flows. For example, consider the following topology:</p>
<p><a class="asset-img-link" href="/brasstacks/slow-drain-due-to-bandwidth-mismatch-and-large-block-reads/6a013487ed263f970c01b8d2778b4d970c.jpg" style="display: inline;"><img alt="One" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b8d2778b4d970c image-full img-responsive" src="/brasstacks/slow-drain-due-to-bandwidth-mismatch-and-large-block-reads/6a013487ed263f970c01b8d2778b4d970c.jpg" title="One" /></a></p>
<p>Host 2 was performing Large Block (512k) sequential READs and was able to get up to about 1600MB/s since both it and the storage array interface&#0160;it was accessing were both running at 16G. This is what we would expect and is completely normal.&#0160;</p>
<p>However, as soon as we added Host 1 (connected at 4G) and started to perform the same Large Block Sequential READs to a 16G target, the throughput for Host 2 dropped to about 400MB/s! During this timeframe we noticed the tim_txcrd_z (Time spent at Zero BB_Credit) counter incrementing on the E_Port attached to the Brocade switch one hop away. We were then able to reproduce the same symptoms on Cisco switches and noticed that under the same conditions their TxWait counter would increment.</p>
<p><a class="asset-img-link" href="/brasstacks/slow-drain-due-to-bandwidth-mismatch-and-large-block-reads/6a013487ed263f970c01bb09904f09970d.jpg" style="display: inline;"><img alt="Two" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb09904f09970d image-full img-responsive" src="/brasstacks/slow-drain-due-to-bandwidth-mismatch-and-large-block-reads/6a013487ed263f970c01bb09904f09970d.jpg" title="Two" /></a></p>
<p>As we dug into the root cause of this behavior, we realized that even though the 4G adapter was running at 4Gb/s, it was requesting data from the array that would ordinarily result in a much higher rate. In fact, we believed, and then were subsequently able to prove, that the 4G adapter was requesting data at a rate that would have resulted in a data rate of 16Gb/s!! How did we prove this? We increased the link speed of Host 1 to 16G and then noticed that both adapters were receiving data at a rate of 1600 MB/s. We also confirmed with the adapter vendors (that we tested) that they do not take link speed or block size into account when transmitting READ requests. So, while in this configuration, there was effectively a bandwidth mismatch of about 1200 MB/s and it’s interesting to note that Host 2’s throughput dropped to the same as that of Host 1. This is typical for this kind of BW mismatch scenario.</p>
<p><strong>So what should you do?</strong></p>
<p>You need to monitor for oversubscription!</p>
<p>Which as it turns out is much easier said than done.&#0160;</p>
<p>Here’s the problem. From the switches point of view, if the 4G adapter (in above example) is running near line rate and returning R_RDY’s regularly, then it’s not doing anything wrong and you probably won’t even see high bb_cred_z or TxWait at switch port connected to Host 1. As a result, in order to monitor for this kind of a condition, you need to monitor the F_Ports connected to the end devices (host and storage port) for high utilization (e.g., &gt;= 95%) and also monitor the ISLs (E_Ports) for signs of congestion that would be similar to what we described in the <a href="https://support.emc.com/kb/464246">slow drain due to lost credit KB article 464246</a>&#0160;(i.e., a ratio of “time spent a zero transmit credit”:”frames transmitted” that is greater than .02)</p>
<p>If you’d like a bit more detail regarding how to do this in a Cisco environment, see the<a href="https://www.youtube.com/watch?v=tY7gu16ar_Q&amp;list=PL1F6F23C54113557F&amp;index=1"> Identifying Slow Drain with Connectrix MDS video</a>.</p>
<p>In part 2 of this series we’ll discuss how to prevent, detect and remediate slow drain due to oversubscription. If you’d like a preview of this information, join Alan and I at Dell EMC World for our “<strong>Configuring your SAN to support all Flash Arrays</strong>” session where we’ll dive into the details of the following slide.</p>
<p>&#0160; <a class="asset-img-link" href="/brasstacks/slow-drain-due-to-bandwidth-mismatch-and-large-block-reads/6a013487ed263f970c01b8d2778ba4970c.jpg" style="display: inline;"><img alt="Stmtlt" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b8d2778ba4970c image-full img-responsive" src="/brasstacks/slow-drain-due-to-bandwidth-mismatch-and-large-block-reads/6a013487ed263f970c01b8d2778ba4970c.jpg" title="Stmtlt" /></a><br /><br /></p>
<p>The session information is:</p>
<p>Tuesday May 9<sup>th</sup>, 8:30-9:30 AM</p>
<p>Thursday May 11<sup>th</sup>, 8:30-9:30 AM</p>
<p>You can also join us for an open discussion on this topic during our Birds-of-a-feather session which is:</p>
<p>Tuesday May 9<sup>th</sup>, 1:30-2:30 PM</p>
<p>Thanks for reading!</p>
<p>&#0160;</p>
