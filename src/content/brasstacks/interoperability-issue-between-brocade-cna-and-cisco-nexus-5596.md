---
title: "Interoperability issue between Brocade CNA and Cisco Nexus 5596"
pubDate: 2011-06-30
postedAt: "03:29 PM"
description: "The other day one of my colleagues, Mugdha Kulkarni, brought an interoperability issue to my attention involving a Brocade 1010 / 1020 CNA (Windows Server 2008, Driver 2.3.0.2) and a Cisco Nexus 5596 (NX-OS 5.0(3)N1(1c)). The problem was the Brocade CNA was unable to login to the Nexus 5596. Complicating..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2011/06/interoperability-issue-between-brocade-cna-and-cisco-nexus-5596.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250913172504/https://brasstacksblog.typepad.com/brass-tacks/2011/06/interoperability-issue-between-brocade-cna-and-cisco-nexus-5596.html"
pdf: "/brasstacks/interoperability-issue-between-brocade-cna-and-cisco-nexus-5596/interoperability-issue-between-brocade-cna-and-cisco-nexus-5596.pdf"
comments:
  - author: "joel"
    date: "07/06/2011 at 10:04 AM"
    html: |-
      <p>Hello,</p>
      <p>we&#39;re thinking of replacing our Brocade 200e for a 5596. we&#39;ll be using them primarily for storage traffic (native fc). how do like them? is there anything that you dislike?</p>
  - author: "Erik Smith"
    date: "07/06/2011 at 02:12 PM"
    html: |-
      <p>Hi Joel, we are actually in the process of qualifying the 5596 for use as an all FC switch.  If all goes well we should be supporting this in September.  So far the testing has gone well.  We already support native FC connections from hosts and storage to the 5596, so the rest of the testing to be done seems fairly low risk to me.  </p>
      <p>In general if you&#39;re comfortable with MDS, you&#39;re going to be comfortable with the 5596.</p>
      <p>I&#39;m curious about your use case / decision criteria for moving from the 300 to the 5596?  If you&#39;d rather exchange email on the topic, you can reach me at erik(dot)smith@emc(dot)com.  </p>
  - author: "Thomas Raabo"
    date: "12/05/2011 at 03:15 PM"
    html: |-
      <p>what twinax cable do you use from nexus to brocade cna</p>
  - author: "Erik Smith"
    date: "12/05/2011 at 04:05 PM"
    html: |-
      <p>Hi Thomas, see the following: <a href="https://web.archive.org/web/20250913172504/https://brasstacksblog.typepad.com/brass-tacks/2011/06/twinax-support-table-6282011.html.html" rel="nofollow">http://brasstacksblog.typepad.com/brass-tacks/2011/06/twinax-support-table-6282011.html.html</a> </p>
      <p>You can use EMC 1, 3 and 5 meter cables.</p>
      <p>Regards, Erik </p>
  - author: "vijay"
    date: "04/25/2012 at 11:39 PM"
    html: |-
      <p>Hi, has the driver version 3.0.3.0 been released yet ?</p>
  - author: "Erik Smith"
    date: "05/02/2012 at 08:01 PM"
    html: |-
      <p>Hi Vijay, yes this version should be listed on the ESM.  I tested with this new version and the problem has been resolved.</p>
---

<p>The other day one of my colleagues, Mugdha Kulkarni, brought an interoperability issue to my attention involving a Brocade 1010 / 1020 CNA (Windows Server 2008, Driver 2.3.0.2) and a Cisco Nexus 5596 (NX-OS 5.0(3)N1(1c)).&#0160;</p>
<p>The problem was the Brocade CNA was unable to login to the Nexus 5596.&#0160; Complicating matters was the fact that the problem would not reproduce on a Nexus 5548.&#0160; This was of particular interest to me since based on what we’ve observed (and what we’ve been told by Cisco), the 5548 and 5596 should be identical from a protocol interoperability point of view. &#0160;&#0160;&#0160;&#0160;</p>
<p>With this in mind, I spent a bit of time in the lab yesterday trying to figure out if the problem was related to a specific Nexus platform or NX-OS revision.&#0160; Based on the testing results and after looking at the traces, my working hypothesis is the problem is due to a DCBX version negotiation problem.&#0160;</p>
<p>We are actively working on the problem but unfortunately as of 6/30/2011, there is no workaround.</p>
<p>UPDATE:&#0160; As of 10/19/2011, there is still no workaround for this problem&#0160;but we were able to confirm that the issue is being caused by both devices failing to agree on which version of DCBX to use.&#0160; As with almost all interoperability issues, the problem is being caused by unique characteristics of both implementations.&#0160; As a result,&#0160;the &quot;fix&quot; for the problem is&#0160;for&#0160;either vendor to slightly alter their DCBX negotiation behavior.&#0160; Also as is typical for these types of interop issues, both vendors are providing a &quot;fix&quot;&#0160;so that&#0160;the issue can be&#0160;addressed in as many different environments as possible.&#0160; With this in mind, I received confirmation from Brocade that this issue will be fixed&#0160;with&#0160;driver version 3.0.3.0 (scheduled to be released early in Q1-2012).&#0160; I also received confirmation from Cisco that this issue will be fixed in their next major NX-OS version (also scheduled to be released early in Q1-2012).&#0160;&#0160;</p>
<p>Thanks for reading!</p>
