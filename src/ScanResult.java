public final class ScanResult {
    public final int port;
    public final String service;
    public final String banner;

    public ScanResult(int port, String service, String banner) {
        this.port = port;
        this.service = service;
        this.banner = banner;
    }
}