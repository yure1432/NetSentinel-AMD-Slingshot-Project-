import java.util.*;

public class JsonSerializer {

    public static String toJson(ScanReport report) {
        StringBuilder sb = new StringBuilder();
        sb.append("{");
        sb.append("\"scanTimestamp\":\"").append(report.scanTimestamp).append("\",");
        sb.append("\"hosts\":[");

        for (int i = 0; i < report.hosts.size(); i++) {
            HostReport host = report.hosts.get(i);

            sb.append("{");
            sb.append("\"ip\":\"").append(host.ip).append("\",");
            sb.append("\"status\":\"up\",");
            sb.append("\"ports\":[");

            for (int j = 0; j < host.ports.size(); j++) {
                ScanResult r = host.ports.get(j);

                sb.append("{");
                sb.append("\"port\":").append(r.port).append(",");
                sb.append("\"service\":\"").append(r.service).append("\",");
                sb.append("\"banner\":");

                if (r.banner == null) {
                    sb.append("null");
                } else {
                    sb.append("\"").append(escape(r.banner)).append("\"");
                }

                sb.append("}");

                if (j < host.ports.size() - 1) sb.append(",");
            }

            sb.append("]}");

            if (i < report.hosts.size() - 1) sb.append(",");
        }

        sb.append("]}");
        return sb.toString();
    }

    private static String escape(String s) {
        return s.replace("\\", "\\\\").replace("\"", "\\\"");
    }
}