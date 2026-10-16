---
title: "Twinax support table"
pubDate: 2011-01-06
postedAt: "04:29 PM"
description: "In my last post, I provided information that described which twinax cables were supported in a number of different configurations. Recently, Mark Lippitt and I debated the best way to present this information in the February edition of the FCoE TechBook, and decided that creating a table made the most..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2011/01/twinax-support-table.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250914140533/https://brasstacksblog.typepad.com/brass-tacks/2011/01/twinax-support-table.html"
pdf: "/brasstacks/twinax-support-table/twinax-support-table.pdf"
comments:
  - author: "JeffS"
    date: "01/07/2011 at 11:18 AM"
    html: |-
      <p>This is such PITA. When vendors started this trend with SPF optics, at least as long as you had the right SFP in each vendor&#39;s product you were good to go. Now we&#39;re dealing with a monolithic cable where it&#39;s &quot;vendor x&quot; on both ends. This could become very complicated should one get into a situation where the two vendors you wish to connect together don&#39;t support each other&#39;s twinx cables. It wouldn&#39;t surprise me to see vendors do this for competitive reasons i.e. if customer can&#39;t use twinx to connect a Cisco to Juniper, would it impact the customer&#39;s decision to use multi-vendor solutions.</p>
      <p>I think it&#39;s a shame that EMC followed this trend by not supporting the passive Cisco cables on the CX. As a customer, this becomes a spare nightmare since I must now keep more than one type/vendor cable in stock. Now I have to keep Cisco and EMC cables around to cover all possibilities. Toss in another vendor and the support matrix continues to expand.</p>
      <p>Oh, and while you&#39;re at it, now that Cisco UCS 1.4 supports direct connection of FCoE storage, you&#39;ll need to update the matrix to include the UCS Fabric Interconnects (FIs)... and the support matrix expands.</p>
  - author: "Erik Smith"
    date: "01/07/2011 at 04:40 PM"
    html: |-
      <p>Hi Jeff, I completely agree that this is going to be a nightmare going forward and I highly encourage you to continue to voice your dissatisfaction!  </p>
      <p>One point worth clarifying, EMC&#39;s reason for not supporting a passive cable is strictly technical.  Our design was optimized for optical connections and this impacts our ability to support a passive cable.  </p>
      <p>A question for you, do you believe that co-locating CLARiiON and an FCoE switch within 5m of each other is something that you will be doing in your environment on a regular basis?  Please send me an email at erik.smith@emc.com if you’d rather take this offline.<br />
      </p>
  - author: "JeffS"
    date: "01/07/2011 at 10:16 PM"
    html: |-
      <p>Erik,</p>
      <p>In my environment, my CX4-240 is next to the rack with my Cisco UCS, so there are only a few feet between them. Even if the CX4 was three racks away, 5m is still manageable. The only advantage I see to the active cable is that the diameter is smaller, so in dense deployments, it may make a difference for cable management and/or cooling. Then again, active cables are more expensive, so I&#39;d rather not be forced into using them when unnecessary at lengths &lt;= 5m. And by &quot;optimized for optical&quot; I take it that implies the appropriate PHY hardware to drive the passive cable was not part of the card&#39;s design?</p>
      <p>I believe an active cable consumes more power ( about 1w per side) over a passive cable. While a few cables from the EMC SAN isn&#39;t going to kill me, it is power that could be saved on the 5M or less runs.</p>
      <p>In the perfect world, every device would support both active and passive cables of appropriate lengths, and from any vendor. Hopefully the next rev of your FCoE adapter will include support for passive cables, and from the vendor of my choice. :)</p>
      <p>If that doesn&#39;t happen, I predict a black-market for twinx cables where one end will report it&#39;s vendor A (in vendor a&#39;s gear), and the other reports vendor B (in vendor b&#39;s gear)!</p>
  - author: "Erik Smith"
    date: "01/11/2011 at 02:33 PM"
    html: |-
      <p>Hi Jeff, your point is taken regarding our support for passive twinax.  We will be taking your feedback into consideration going forward.  In regard to your concerns about power, I discussed this with a couple of people in our hardware group and you’re right, active twinax does consume more power than passive twinax.  In the case of a passive twinax cable, the necessary hardware to support driving the signal is included in the PHY and consume about 100mW per port.  As an aside, the iSCSI SLIC used in our CLARiiON array implements this technology. In the case of an active twinax cable, such as the one used with the FCoE  SLIC, the components for driving the signal are moved into the cable and consume about 200mW per port.</p>
  - author: "JeffS"
    date: "01/13/2011 at 11:53 AM"
    html: |-
      <p>Thanks Erik... I appreciate the feedback, and hope that more universal support can be implemented, avoiding the growing  twinax &quot;matrix of pain&quot; documents each vendor is now publishing.  </p>
      <p>Here&#39;s an example of one customers pain:<br />
      <a href="http://robertjuric.com/2010/11/02/twinaxdac-cable-differences/" rel="nofollow">http://robertjuric.com/2010/11/02/twinaxdac-cable-differences/</a></p>
      <p>Jeff</p>
---

<p>In my <a href="/brasstacks/should-i-use-optical-fiber-or-twinax-cable/" target="_self">last post</a>, I provided information that described which twinax cables were supported in a number of different configurations.&#0160; Recently, Mark Lippitt and I debated the best way to present this information in the February edition of the <a href="http://www.emc.com/collateral/hardware/technical-documentation/h6290-fibre-channel-over-ethernet-techbook.pdf" target="_self">FCoE TechBook</a>, and decided that creating a table made the most sense. The result of this work is shown below.&#0160;</p>
<p>In addition, I&#0160;agree with <a href="https://web.archive.org/web/20250914140533/https://brasstacksblog.typepad.com/brass-tacks/2010/12/should-i-use-optical-fiber-or-twinax-cable.html?cid=6a013487ed263f970c0147e11e773c970b#comment-6a013487ed263f970c0147e11e773c970b" target="_self">Andrew Fidel’s comment</a>.&#0160; The fact that we need a table for cable support is <em>very </em>frustrating and is something that should be resolved in the future.&#0160; Unfortunately, the switch manufacturers aren’t listening.&#0160; Who knows…maybe they could be convinced to make a change if “twinax support tables” becomes a recurring complaint during conversations with their end users.&#0160; But for now, we’re stuck with it.</p>
<p style="text-align: center;"><a href="/brasstacks/twinax-support-table/6a013487ed263f970c0147e154bf99970b.jpg" style="display: inline;"><img alt="Table" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0147e154bf99970b" src="/brasstacks/twinax-support-table/6a013487ed263f970c0147e154bf99970b.jpg" title="Table" /></a>&#0160;<br /><a href="/brasstacks/twinax-support-table/6a013487ed263f970c0147e154bfe7970b.jpg" style="display: inline;"><img alt="Legend" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0147e154bfe7970b" src="/brasstacks/twinax-support-table/6a013487ed263f970c0147e154bfe7970b.jpg" title="Legend" /></a>&#0160;</p>
<p>Thanks for reading!</p>
<p>Update:&#0160; In case you need them, the model numbers for the EMC Twinax cables are included below:</p>
<p><a href="/brasstacks/twinax-support-table/6a013487ed263f970c014e6051c690970c.jpg" style="display: inline;"><img alt="ModelNumbers" border="0" class="asset  asset-image at-xid-6a013487ed263f970c014e6051c690970c" src="/brasstacks/twinax-support-table/6a013487ed263f970c014e6051c690970c.jpg" title="ModelNumbers" /></a>&#0160;</p>
