import java.util.List;

public final class ScanReport {
    public final String scanTimestamp;
    public final List<HostReport> hosts;

    public ScanReport(String scanTimestamp, List<HostReport> hosts) {
        this.scanTimestamp = scanTimestamp;
        this.hosts = hosts;
    }
}