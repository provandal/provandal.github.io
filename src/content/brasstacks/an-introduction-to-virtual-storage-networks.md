---
title: "An Introduction to Virtual Storage Networks"
pubDate: 2014-04-16
postedAt: "04:21 PM"
description: "I recently started a VSN blog series that describes (in great detail) a new concept that we’re referring to as a Virtual Storage Network or VSN. As I was writing the third installment in the series, I realized the approach I was using to define the VSN concept was analogous..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2014/04/an-introduction-to-virtual-storage-networks.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250912233546/https://brasstacksblog.typepad.com/brass-tacks/2014/04/an-introduction-to-virtual-storage-networks.html"
pdf: "/brasstacks/an-introduction-to-virtual-storage-networks/an-introduction-to-virtual-storage-networks.pdf"
comments: []
---

<p>I recently started a <a href="/brasstacks/virtual-storage-networks-part-1/">VSN blog series</a> that describes (in great detail) a new concept that we’re referring to as a Virtual Storage Network or VSN.&#0160; As I was writing the third installment in the series, I realized the approach I was using to define the VSN concept was analogous to trying to describe a forest by starting with a description of soil composition.&#0160; Although this approach might have eventually led to some kind of understanding of what I was talking about, I began to feel that I was probably going to lose the vast majority of readers if I didn’t take a different tack.&#0160; With this in mind, this post will provide a very high level overview of the VSN concept, describe what we’re trying to accomplish and hopefully provide a framework to allow readers to understand the more detailed <a href="/brasstacks/virtual-storage-networks-part-1/">VSN series</a>.&#0160;</p>
<h2>Why VSN?</h2>
<p>Since Fibre Channel was first introduced, the need to manually configure FC connectivity (e.g., <a href="/brasstacks/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san/">create zones</a>) has not only proven to be unpopular with customers, it has also proven to be a barrier to innovation.&#0160;</p>
<p>From a customer’s point of view, many view zoning as just an additional administrative burden and have been asking for a way to eliminate the <span style="text-decoration: underline;">manual process</span> of zoning for years.&#0160; We’ve responded to these requests by:</p>
<ul>
<li>introducing products such as Volume Logix, ECC SAN Manager and ViPR;</li>
<li>participating in industry initiatives (e.g., <a href="http://www.t11.org/ftp/t11/pub/fc/scm/07-430v3.pdf">FC-SCM</a>) intended to eliminate zoning; and</li>
<li>inventing a new mechanism (<a href="/brasstacks/introducing-target-driven-zoning-tdz/">TDZ</a>) that automates zone creation</li>
</ul>
<p>As we were standardizing TDZ, we asked other EMC engineers for input and were surprised to discover that&#0160;many of them were interested in the approach because they had run into problems with zoning in the past. &#0160;In fact, several of them had considered adding functionality but avoided doing so specifically because of zoning. &#0160;On the opposite end of the spectrum there was at least one case of an engineer scripting the zoning commands required for their particular use case. &#0160;While their script worked fine, ultimately I think they were just cleaning up someone else&#39;s mess and thought it was a shame that they had to spend time working around a limitation that should have been addressed long ago. &#0160;</p>
<p>A more recent example of the barrier to innovation is&#0160;the <a href="/brasstacks/fast-sideways-a-connectivity-point-of-view/">FAST sideways</a> use case; it takes no less than four connectivity (e.g., zoning) changes in order to migrate a storage volume from one array to another. &#0160;Until these connectivity changes can be automated (e.g., via ViPR); FAST sideways will probably not be all that useful as a automated remediation mechanism for chronic issues with IOPS or RT due to an overloaded array.</p>
<p>Although zoning is something that is specific to FC and FCoE, other types of storage protocols also suffer from the need to manually configure connectivity.&#0160; I described the challenges with iSCSI in the <a href="/brasstacks/fc-and-fcoe-versus-iscsi-network-centric-versus-end-node-centric-provisioning/">FC and FCoE versus iSCSI – “Network-centric” versus “End-Node-centric” provisioning blog post</a> and I described the challenges for FC, FCoE, iSCSI and File in the <a href="/brasstacks/a-thought-experiment-the-universal-fabric/">Universal Fabric Controller blog post</a>.</p>
<p>While these manual connectivity configuration steps have proven to be burdensome to our Enterprise customers, to our Service Provider customers, they’re anathema.&#0160; This is because many of these Service Providers are gearing up to compete with the likes of&#0160;<a href="http://aws.amazon.com/">Amazon</a> and in order for them to complete effectively, they need to be able to:</p>
<ol>
<li>Completely automate the end-to-end provisioning process (including storage provisioning); and</li>
<li>Provide services at a price that are difficult to match when using traditional infrastructure components.</li>
</ol>
<p>As a result, many of these customers are not interested in FC or FCoE because they perceive it to be a more expensive and less flexible solution, due to the perceived manual provisioning steps, specialized skill sets and specialized hardware associated with it.&#0160;</p>
<p>Actually, if you press them for what they really want in regards to storage features, many just want storage arrays to go away and have the storage capacity provided via a software based approach.&#0160; I’ll generically refer to this approach as <a href="http://wikibon.org/wiki/v/Server_SAN_Market_Definition">Server SAN</a> and point out that EMC has a product in this space called <a href="http://www.emc.com/storage/scaleio/index.htm">ScaleIO</a>.&#0160; I’ll also point out that VMware has a solution called <a href="http://www.vmware.com/products/virtual-san?cid=70180000000NM8c&amp;src=paidsearch_vsan_google_awareness_us&amp;mkwid=sBExJOxgM&amp;pcrid=37586918777&amp;kw=vsan&amp;mt=p&amp;utm_source=google&amp;utm_medium=cpc&amp;utm_term=vsan&amp;utm_content=37586918777&amp;utm_campaign=GS_VMVSAN_AMS_US_EN_P_">VSAN</a> which has been on our radar for some time.&#0160; Both of these products (along with <a href="http://ceph.com/">CEPH</a>) have proven to be very popular (at least conceptually) with Customers in both the Enterprise and Service Provider spaces.&#0160; I think the main reason for the interest is <a href="https://www.youtube.com/watch?v=1EDWKE93ivw">ease of use</a>.&#0160;</p>
<p>I’ll admit that I’m intrigued by the Server SAN concept and I see use cases for both ScaleIO and VSAN.&#0160; But I also have to admit, as I discuss in <a href="/brasstacks/virtual-storage-networks-part-1/">part 1</a> of the VSN series, I have concerns about the ability of Server SAN solutions to provide Enterprise class features.&#0160; That having been said, the message from our customers is crystal clear “<strong>Make it easier to consume your array based storage or we’ll find another solution</strong>”…</p>
<p>I’ll spare you some of the details and simply say that we took this message to heart. &#0160;We did a bunch of work gathering connectivity requirements from customers (including at EMC World last year) to figure out what the best approach would be.&#0160; As we were doing this an interesting pattern started to emerge:</p>
<p>Enterprise Customers (in general):</p>
<ul>
<li>Really like Fibre Channel</li>
<li>Really do NOT like iSCSI</li>
<li>Are willing to use FCoE at least from the Server to the ToR switch</li>
<li>Are interested in investigating approaches to automate zoning</li>
<li>Are increasingly looking at File</li>
<li>Are looking at Server SAN to see what it can do for them but generally like the automation aspect of it</li>
<li>Are typically very conservative when it comes to new technology</li>
<li>See connectivity from Server to a Storage array as something that is static.</li>
<li>Have a wide range of requirements with regards to multi-tenancy.&#0160; Generally they see it as something that is handled through orchestration and not necessarily something that needs to extend to the data plane.</li>
</ul>
<p>Service Providers (in general):</p>
<ul>
<li>Really like the Server San concept</li>
<li>Like iSCSI, File, Object – will use whatever provides adequate performance and is easiest</li>
<li>Really do not like FC – There are exceptions (e.g., Rackspace hybrid cloud and at least to some degree vCHS)</li>
<li>Are not conservative when it comes to new technology</li>
<li>See connectivity from Server to Storage as dynamic</li>
<li>Have many multi-tenant storage requirements.&#0160; Generally they see multi-tenancy as something that is handled through orchestration but also want data plane isolation as I describe in <a href="/brasstacks/virtual-storage-networks-part-1/">Part 1</a>.</li>
</ul>
<p>In order to satisfy both the Enterprise and SP requirements, it became clear that we would need a solution that could support multiple protocols and automate connectivity tasks for all of them.&#0160; Not only that, we would need something that makes our arrays as simple to use a Server SAN solution.&#0160;</p>
<p>Simple, right? &lt;/sarcasm&gt;</p>
<p>With these requirements in mind, we set a goal for the VSN project to:</p>
<ul>
<li>enable the dynamic creation of storage service compositions;</li>
<li>automate connectivity between compute and these storage service compositions; and</li>
<li>do so in a way that is compatible with the concept of multi-tenant storage.</li>
</ul>
<p>In case you&#39;re wondering, a storage service composition is a collection of storage services that are presented to an end user as a single storage volume.&#0160; For the purposes of this discussion, think of a storage service composition as a storage volume that has specific attributes.&#0160; These attributes could include:</p>
<ul>
<li><a href="https://en.wikipedia.org/wiki/IOPS">Input/Output Operations Per Second (IOPS)</a></li>
<li><a href="http://www.emc.com/corporate/glossary/replication.htm">Replication</a></li>
<li><a href="http://www.emc.com/corporate/glossary/data-deduplication.htm">Data Deduplication</a></li>
<li><a href="https://en.wikipedia.org/wiki/Recovery_time_objective">Recovery Time Objective (RTO)</a></li>
<li><a href="https://en.wikipedia.org/wiki/Recovery_point_objective">Recovery Point Objective (RPO)</a></li>
<li>And many more…</li>
</ul>
<p>One example of a storage service composition that has been automatically attached to a compute instance is shown below and is described in <a href="/brasstacks/virtual-storage-networks-part-2-requirements-for-multi-tenant-storage/">Part 2 of the VSN series</a>&#0160;in the &quot;Storage Service Insertion&quot; section.&#0160;</p>
<p><a class="asset-img-link" href="/brasstacks/an-introduction-to-virtual-storage-networks/6a013487ed263f970c01a511a11961970c.jpg" style="display: inline;"><img alt="One" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01a511a11961970c image-full img-responsive" src="/brasstacks/an-introduction-to-virtual-storage-networks/6a013487ed263f970c01a511a11961970c.jpg" title="One" /></a></p>
<p>The key take away from the above diagram is each hypervisor would only see a single “gray” Virtual Volume on the VPLEX.&#0160; The storage capacity for the Virtual Volume actually resides on the VMAX.&#0160; The VMAX could then be getting deduplication services from Data Domain.&#0160; I refer to the Virtual Volume, the capacity service on the VMAX and the deduplication service on Data Domain as a “Storage Service Composition”.&#0160;</p>
<p>I have not (yet) attempted to calculate how many possible storage compositions could be created from just EMC products alone, but there are many others possible.&#0160; It’s important to note that from a connectivity automation point of view, the number and type of services doesn’t really matter as long as the two services can use a common protocol (e.g., FC, iSCSI, File, Object, etc) to communicate with one another.</p>
<h2>Conclusion</h2>
<p>Well, that’s about as close to the forest of Virtual Storage Networks that I can get without getting back into a study of soil composition.&#0160; If you were to remember only a couple of things about this post, I would like them to be:</p>
<ul>
<li>The purpose of the Virtual Storage Network concept is to make storage and storage service compositions as easy to use as possible</li>
<li>VSNs will be compatible with both Enterprise and Service Provider environments</li>
<li>&#0160;A Virtual Storage Network can be created using any of the supported protocols today
<ul>
<li>There are limits to this and they will be discussed in parts 3 and 4 of the series.</li>
</ul>
</li>
<li>Virtual Storage Networks do not have inherent orchestration layer dependencies</li>
</ul>
<p>If you’re interested in more information please see the more detailed <a href="/brasstacks/virtual-storage-networks-part-1/">VSN series</a>.&#0160;</p>
<p>Thanks for reading!</p>
