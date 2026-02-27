import java.util.List;

public final class HostReport {
    public final String ip;
    public final List<ScanResult> ports;

    public HostReport(String ip, List<ScanResult> ports) {
        this.ip = ip;
        this.ports = ports;
    }
}