---
title: "First you must enable RAID, before you can disable it."
pubDate: 2012-02-23
postedAt: "01:32 PM"
description: "Before you jump into this post thinking a \"storage guy\" is in any way recommending that you disable RAID on your array, please understand that I’m talking about disabling \"SW RAID\" on a server ONLY! I’m writing this as penance for spending far too much time on this problem. To..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2012/02/first-you-must-enable-raid-before-you-can-disable-it.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250910234845/https://brasstacksblog.typepad.com/brass-tacks/2012/02/first-you-must-enable-raid-before-you-can-disable-it.html"
pdf: "/brasstacks/first-you-must-enable-raid-before-you-can-disable-it/first-you-must-enable-raid-before-you-can-disable-it.pdf"
comments:
  - author: "Tatersolid"
    date: "04/09/2012 at 09:05 AM"
    html: |-
      <p>This is an example of what I call &quot;the lost art of sensible defaults&quot;. In my entire 20 year IT career, it&#39;s never been this bad. No matter what the system - be it a switch, router, storage array, commercial or open source OS, or white-box server BIOS - the defaults are very rarely usable or even rational. You either have to spend an inordinate amount of time disabling features or &quot;hardening&quot; things. Or spend the same amount of time doing the opposite, enabling every possible feature and sub-feature one at a time (I&#39;m looking at you Win 2008 R2).</p>
      <p>It&#39;s a massive, coordinated industry failure. Provides job security I suppose.</p>
  - author: "Erik Smith"
    date: "05/02/2012 at 07:58 PM"
    html: |-
      <p>Hi, thanks for taking the time to comment and apologies for taking so long to approve and respond.</p>
      <p>I agree this type of problem is very frustrating when encountered and I run into them too often...</p>
      <p>Erik</p>
---

<p><em>Before you jump into this post thinking a &quot;storage guy&quot; is in any way recommending that you disable RAID on your array, please understand that I’m talking about disabling &quot;SW RAID&quot; on a server ONLY!</em></p>
<p>I’m writing this as penance for spending far too much time on this problem.&#0160; To make matters worse, in the end I had to rely on the help of a couple of colleagues to figure out what I was doing wrong.&#0160; Thanks Tom McSweeney and Pat Mullaney!</p>
<p>While trying to install SLES11 SP1 onto a generic white box Intel based server, the installer prompted me to select a hard disk.&#0160; The problem was, both of the devices I could select were “BIOS RAID” (see below).&#0160; Now while I’m sure there are some people who would never think about installing an OS onto anything but a BIOS SW RAID disk, I’m not currently one of them, and as a result I wanted to disable this feature.&#0160;</p>
<p><a href="/brasstacks/first-you-must-enable-raid-before-you-can-disable-it/6a013487ed263f970c0168e7dcc245970c.jpg" style="display: inline;"><img alt="One" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0168e7dcc245970c" src="/brasstacks/first-you-must-enable-raid-before-you-can-disable-it/6a013487ed263f970c0168e7dcc245970c.jpg" title="One" /></a></p>
<p>Seeing as how “BIOS” was in the name of the device, I figured the appropriate place to look for a “disable BIOS RAID” setting would be in the BIOS.&#0160; So I power cycled the server and hit &lt;F2&gt; at the appropriate time.</p>
<p>After looking over each option in all of various tabs, I discovered the closest match was under <strong>Advanced/SATA</strong> mode.&#0160; Upon seeing that it was set to <strong>ENHANCED</strong>, I&#0160;said to myslef &quot;well, that settings fine&quot; and then proceeded to waste the better part of a day changing other settings, rebooting, cursing, etc. &#0160;&#0160;After each set of changes I would restart the install and in all cases the BIOS RAID devices remained.</p>
<p><a href="/brasstacks/first-you-must-enable-raid-before-you-can-disable-it/6a013487ed263f970c016301e5f2f7970d.jpg" style="display: inline;"><img alt="Two" border="0" class="asset  asset-image at-xid-6a013487ed263f970c016301e5f2f7970d image-full" src="/brasstacks/first-you-must-enable-raid-before-you-can-disable-it/6a013487ed263f970c016301e5f2f7970d.jpg" title="Two" /></a></p>
<p>As I was preparing to do something drastic, I figured I would try one last thing and put out a “please help me before I jump out of the window” request to Pat and Tom.&#0160; Eventually Tom came back with the answer that pointed me in the right direction.&#0160; To make a long story short, you have to enable <strong>SW RAID</strong> in order for the BIOS RAID configuration utility to be displayed during boot.&#0160; Once you are in the BIOS RAID configuration utility, you can delete the BIOS RAID devices and they will no longer be displayed when you attempt to install.&#0160;</p>
<p>The step-by-step instructions are:</p>
<p>1. Set the SATA mode under the Advanced tab in the &lt;F2&gt; setup screen to SW RAID.</p>
<p><a href="/brasstacks/first-you-must-enable-raid-before-you-can-disable-it/6a013487ed263f970c0168e7dcc2f5970c.jpg" style="display: inline;"><img alt="Three" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0168e7dcc2f5970c image-full" src="/brasstacks/first-you-must-enable-raid-before-you-can-disable-it/6a013487ed263f970c0168e7dcc2f5970c.jpg" title="Three" /></a></p>
<p>2. Save the changes to the BIOS and reboot.</p>
<p>3. Hit &lt;CTRL-E&gt; when prompted to enter the Embedded RAID configuration utility.&#0160; <strong>BY THE WAY</strong> this option is&#0160;<strong>NOT AVAILABLE</strong>&#0160;when SW RAID is disabled.&#0160; <strong>WHICH IS SO FRUSTRATING</strong> (but in hindsight completely understandable)</p>
<p><a href="/brasstacks/first-you-must-enable-raid-before-you-can-disable-it/6a013487ed263f970c016301e5f41f970d.jpg" style="display: inline;"><img alt="Four" border="0" class="asset  asset-image at-xid-6a013487ed263f970c016301e5f41f970d image-full" src="/brasstacks/first-you-must-enable-raid-before-you-can-disable-it/6a013487ed263f970c016301e5f41f970d.jpg" title="Four" /></a>&#0160;&#0160;</p>
<p>4. Once in the utility, select:</p>
<ul>
<li>“Configure”</li>
<li>“Clear Configuration” (then confirm the change)</li>
<li>Hit “esc” twice and then &lt;CTRL&gt;&lt;ALT&gt;&lt;DEL&gt; to save the configuration and reset.&#0160; </li>
</ul>
<p>5. Hit &lt;F2&gt; at the appropriate time to enter into the BIOS setup and then change the SATA mode back to ENHANCED (or whatever you want).</p>
<p>Thanks for reading!</p>
