---
title: "How to determine a switch's role in a Clos network with MLAG’d leaves"
pubDate: 2017-11-29
postedAt: "02:57 PM"
description: "A group of us have been experimenting with IP Fabrics recently and I'm curious to know if anyone has used the following approach or knows of work that accomplishes the same goal in a different way. When initializing an IP Fabric, one of the first decisions that needs to be..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2017/11/how-to-determine-a-switchs-role-in-a-clos-network-with-mlagd-leaves.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250910165432/https://brasstacksblog.typepad.com/brass-tacks/2017/11/how-to-determine-a-switchs-role-in-a-clos-network-with-mlagd-leaves.html"
pdf: "/brasstacks/how-to-determine-a-switchs-role-in-a-clos-network-with-mlagd-leaves/how-to-determine-a-switchs-role-in-a-clos-network-with-mlagd-leaves.pdf"
comments: []
---

<p>A group of us have been experimenting with IP Fabrics recently and I&#39;m curious to know if anyone has used the following approach or knows of work that accomplishes the same goal in a different way.&#0160;&#0160;</p>
<p>When initializing an IP Fabric, one of the first decisions that needs to be made concerns the switch role (e.g., is this a leaf or a spine switch).&#0160; There are multiple approaches that could be used to aid with this decision:</p>
<ol>
<li>Rely on the factory to preset the personality of each switch before it is shipped. The challenge with this approach is that it requires additional information to be supplied by the customer and consumed by the technician in the factory.</li>
<li>Rely on the customer to identify the switch roles (e.g., via MAC Address) as racks are being installed. This approach could be perceived as burdensome to the customer.</li>
<li>Determine the switch role programmatically and allow the customer to override the switch roles if necessary.&#0160; The diagram below and the explanation following it provide an overview of how this might be possible if we assume MLAG’d leaves are going to be a part of the topology.</li>
</ol>
<p><a class="asset-img-link" href="/brasstacks/how-to-determine-a-switchs-role-in-a-clos-network-with-mlagd-leaves/6a013487ed263f970c01b7c9388144970b.jpg" style="display: inline;"><img alt="Picture1" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01b7c9388144970b image-full img-responsive" src="/brasstacks/how-to-determine-a-switchs-role-in-a-clos-network-with-mlagd-leaves/6a013487ed263f970c01b7c9388144970b.jpg" title="Picture1" /></a></p>
<p>&#0160;</p>
<p>Step 0: Every switch will provide the Network Controller with the list of switches it is connected to.&#0160; This information can be gathered via LLDP.&#0160;</p>
<p>Step 1: The Network Controller will separate the switches into two groups; the first group (i.e., A, B and C) will be connected to a common set of other switches (i.e., D, E, F, G, H, I), the second group (i.e., D, E, F, G, H, I) will not be connected to a common set of switches.&#0160;</p>
<p>Step 2: Label the common set of switches that the first group is connected to as set Ω and understand that anything connected to Ω is a spine switch and should be included in set Φ.</p>
<p>Step 3: For each member in Ω, remove the members of Φ from its list of connected members.</p>
<p>Step 4: For each member in Ω, use the remaining switch in the list of connected members as its MLAG partner.</p>
<p>Comments welcome!</p>
