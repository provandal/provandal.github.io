---
title: "The power of Layers"
pubDate: 2017-12-05
postedAt: "11:14 AM"
description: "Originally posted by Erik Smith to Brasstacksblog Background I have a thing for breaking down complex topics into “Layers” (e.g., Storage Protocol Stacks). I use this approach because it breaks down what would otherwise be an overwhelming amount of information, into chunks of functionality that I can keep in my..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2017/12/the-power-of-layers.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250911104628/https://brasstacksblog.typepad.com/brass-tacks/2017/12/the-power-of-layers.html"
pdf: "/brasstacks/the-power-of-layers/the-power-of-layers.pdf"
comments: []
---

<h1><span style="font-size: 10pt;">Originally posted by Erik Smith to <a href="/brasstacks/the-power-of-layers/">Brasstacksblog</a></span></h1>
<h1><span style="font-size: 14pt;">Background</span></h1>
<p>I have a thing for breaking down complex topics into “Layers” (e.g., <a href="/brasstacks/storage-protocol-stacks/">Storage Protocol Stacks</a>).&#0160;</p>
<p>I use this approach because it breaks down what would otherwise be an overwhelming amount of information, into chunks of functionality that I can keep in my brain without experiencing a <a href="https://en.wikipedia.org/wiki/Page_fault">page fault</a>.&#0160;</p>
<p>The layering approach also allows me to set boundaries on what I need to know <strong>personally</strong> versus what I can just utilize (i.e., without fully understanding all of the implementation details).&#0160; Put another way, I don’t need to know how to build a bridge, I just need to know how to drive across it.</p>
<p>The concept of layering plays out with macro-level trends; SaaS developers use PaaS, and PaaS developers use IaaS, IaaS developers orchestrate services, and these services are provided by whoever configures the <a href="/brasstacks/the-iaas-missing-link/">IaaS Missing Link</a>, etc.</p>
<p>The concept also works at a micro-level and the architecture of a particular <a href="https://12factor.net/">12-factor app</a> could be one example.</p>
<p>Now, it’s one thing to intellectually understand the concept of layering and quite another to apply the principle to a software architecture or even to a new storage protocol.&#0160; In fact, the work that I did with <a href="/brasstacks/zero-touch-infrastructure-provisioning-ztip/">ZTIP</a> has proven to be some of the hardest and most rewarding in my career, at least from a personal development perspective.&#0160;</p>
<p>I also feel compelled to point out that it is also only because of the work on ZTIP that I can fully appreciate the impact that Claudio Desanti (and perhaps others at Cisco) had on my ability to think along these lines.&#0160; Having the opportunity to watch him create and then easily defend the need for an FCoE Initialization Protocol (FIP) during the T11 standardization process was educational (to completely understate the experience).&#0160; &#0160;&#0160;</p>
<p>Side note: A LONG time ago I blogged about FIP <a href="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/">here</a>, <a href="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-2-fip-snooping-bridges-and-fibre-channel-forwarders/">here</a> and <a href="/brasstacks/yet-another-reason-why-enabling-fip-snooping-is-important-when-using-fcoe/">here</a>.&#0160; In those posts I described how FIP worked, but it wasn’t until a couple of years after I started working with it that I was able to realize that “FIP bridges the gap between the expectations of the FC protocol and the reality of an FCoE topology.”&#0160; It still melts my mind.&#0160; A very humble bow to Claudio.</p>
<h1><span style="font-size: 14pt;">An iSCSI example</span></h1>
<p>In addition to applying the layering principle to a new protocol or software architecture, you can also apply the principle to something as mundane as a set of configuration steps.&#0160; To this end, the series of diagrams that follow will describe how you could apply this principle to the process of configuring iSCSI connectivity on VMAX.&#0160; A h/t to Wei Xiaoyan for collaborating on this with me.</p>
<p>BTW, I think breaking down the configuration steps this way is a GREAT way to figure out how you might automate the configuration of these steps.&#0160;&#0160; In fact, the process being described below was done in preparation for a project that was intended to do just that, but it was shelved for reasons that will be saved for my post retirement book. :-)</p>
<p>Step 1</p>
<p><a class="asset-img-link" href="/brasstacks/the-power-of-layers/6a013487ed263f970c01b7c93a334b970b.jpg" style="display: inline;"><img alt="One" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b7c93a334b970b image-full img-responsive" src="/brasstacks/the-power-of-layers/6a013487ed263f970c01b7c93a334b970b.jpg" title="One" /></a></p>
<p>Step 2</p>
<p><a class="asset-img-link" href="/brasstacks/the-power-of-layers/6a013487ed263f970c01bb09dd50ae970d.jpg" style="display: inline;"><img alt="Two" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb09dd50ae970d image-full img-responsive" src="/brasstacks/the-power-of-layers/6a013487ed263f970c01bb09dd50ae970d.jpg" title="Two" /></a></p>
<p>Step 3</p>
<p><a class="asset-img-link" href="/brasstacks/the-power-of-layers/6a013487ed263f970c01b7c93a335c970b.jpg" style="display: inline;"><img alt="Three" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b7c93a335c970b image-full img-responsive" src="/brasstacks/the-power-of-layers/6a013487ed263f970c01b7c93a335c970b.jpg" title="Three" /></a></p>
<p>Step 4</p>
<p><a class="asset-img-link" href="/brasstacks/the-power-of-layers/6a013487ed263f970c01bb09dd50d9970d.jpg" style="display: inline;"><img alt="Four" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb09dd50d9970d image-full img-responsive" src="/brasstacks/the-power-of-layers/6a013487ed263f970c01bb09dd50d9970d.jpg" title="Four" /></a></p>
<p>Step 5</p>
<p><a class="asset-img-link" href="/brasstacks/the-power-of-layers/6a013487ed263f970c01b7c93a3376970b.jpg" style="display: inline;"><img alt="Five" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b7c93a3376970b image-full img-responsive" src="/brasstacks/the-power-of-layers/6a013487ed263f970c01b7c93a3376970b.jpg" title="Five" /></a></p>
<p>Step 6</p>
<p><a class="asset-img-link" href="/brasstacks/the-power-of-layers/6a013487ed263f970c01bb09dd50ef970d.jpg" style="display: inline;"><img alt="Six" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb09dd50ef970d image-full img-responsive" src="/brasstacks/the-power-of-layers/6a013487ed263f970c01bb09dd50ef970d.jpg" title="Six" /></a></p>
<p>Step 7</p>
<p><a class="asset-img-link" href="/brasstacks/the-power-of-layers/6a013487ed263f970c01b7c93a3397970b.jpg" style="display: inline;"><img alt="Seven" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b7c93a3397970b image-full img-responsive" src="/brasstacks/the-power-of-layers/6a013487ed263f970c01b7c93a3397970b.jpg" title="Seven" /></a></p>
<p>Step 8</p>
<p><a class="asset-img-link" href="/brasstacks/the-power-of-layers/6a013487ed263f970c01b7c93a33a4970b.jpg" style="display: inline;"><img alt="Eight" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b7c93a33a4970b image-full img-responsive" src="/brasstacks/the-power-of-layers/6a013487ed263f970c01b7c93a33a4970b.jpg" title="Eight" /></a></p>
<p>Step 9</p>
<p><a class="asset-img-link" href="/brasstacks/the-power-of-layers/6a013487ed263f970c01b7c93a33ac970b.jpg" style="display: inline;"><img alt="Nine" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b7c93a33ac970b image-full img-responsive" src="/brasstacks/the-power-of-layers/6a013487ed263f970c01b7c93a33ac970b.jpg" title="Nine" /></a></p>
<p>Step 10</p>
<p><a class="asset-img-link" href="/brasstacks/the-power-of-layers/6a013487ed263f970c01b8d2c4894e970c.jpg" style="display: inline;"><img alt="Ten" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b8d2c4894e970c image-full img-responsive" src="/brasstacks/the-power-of-layers/6a013487ed263f970c01b8d2c4894e970c.jpg" title="Ten" /></a></p>
<p>Step 11</p>
<p><a class="asset-img-link" href="/brasstacks/the-power-of-layers/6a013487ed263f970c01bb09dd511f970d.jpg" style="display: inline;"><img alt="Eleven" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb09dd511f970d image-full img-responsive" src="/brasstacks/the-power-of-layers/6a013487ed263f970c01bb09dd511f970d.jpg" title="Eleven" /></a></p>
<p>Step 12</p>
<p><a class="asset-img-link" href="/brasstacks/the-power-of-layers/6a013487ed263f970c01b7c93a33cb970b.jpg" style="display: inline;"><img alt="Twelve" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b7c93a33cb970b image-full img-responsive" src="/brasstacks/the-power-of-layers/6a013487ed263f970c01b7c93a33cb970b.jpg" title="Twelve" /></a></p>
<p>Step 13</p>
<p><a class="asset-img-link" href="/brasstacks/the-power-of-layers/6a013487ed263f970c01bb09dd5137970d.jpg" style="display: inline;"><img alt="Thirteen" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb09dd5137970d image-full img-responsive" src="/brasstacks/the-power-of-layers/6a013487ed263f970c01bb09dd5137970d.jpg" title="Thirteen" /></a></p>
<p>Step 14</p>
<p><a class="asset-img-link" href="/brasstacks/the-power-of-layers/6a013487ed263f970c01bb09dd5141970d.jpg" style="display: inline;"><img alt="Fourteen" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb09dd5141970d image-full img-responsive" src="/brasstacks/the-power-of-layers/6a013487ed263f970c01bb09dd5141970d.jpg" title="Fourteen" /></a></p>
<p>Thanks for reading!</p>
