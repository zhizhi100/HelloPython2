function FindProxyForURL(url, host) {
	if (localHostOrDomainIs(host, "yscportal.hnds.tax.cn")||localHostOrDomainIs(host, "yscdddl.hnds.tax.cn")||localHostOrDomainIs(host, "yschxqd.hnds.tax.cn")||localHostOrDomainIs(host, "ysctycx.hnds.tax.cn")||localHostOrDomainIs(host, "google.com")) {
		return "PROXY 127.0.0.1:8000";
	} else {
		return "DIRECT";
	}
}