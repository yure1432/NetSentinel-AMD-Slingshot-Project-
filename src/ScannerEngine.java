import java.net.*;
import java.time.Instant;
import java.util.concurrent.*;
import java.util.*;

public class ScannerEngine {

    private final ScanConfig config;

    private final ThreadPoolExecutor executor;
    private final SimpleRateLimiter rateLimiter;

    private final ConcurrentHashMap<String, ConcurrentHashMap<Integer, ScanResult>> results = new ConcurrentHashMap<>();
    private final Set<String> aliveHosts = ConcurrentHashMap.newKeySet();

    public ScannerEngine(ScanConfig config) {
        this.config = config;

        this.executor = new ThreadPoolExecutor(
                100,
                100,
                0L,
                TimeUnit.MILLISECONDS,
                new ArrayBlockingQueue<>(5000),
                new ThreadPoolExecutor.CallerRunsPolicy()
        );

        this.rateLimiter = new SimpleRateLimiter(Math.min(config.rateLimitPerSecond, 2000));
    }

    public ScanReport execute() {
        submitJobs();
        executor.shutdown();

        try {
            executor.awaitTermination(7, TimeUnit.DAYS);
        } catch (InterruptedException e) {
            executor.shutdownNow();
            Thread.currentThread().interrupt();
        }

        return buildReport();
    }

    private void submitJobs() {
        long totalHosts = 1L << (32 - config.prefixLength);
        long usableHosts = totalHosts;

        long base = ipToLong(config.networkAddress);

        for (long i = 0; i < usableHosts; i++) {
            long ipLong = base + i;

            if (config.prefixLength != 32) {
                if (i == 0 || i == usableHosts - 1) continue;
            }

            String ip = longToIp(ipLong);

            for (int port = config.startPort; port <= config.endPort; port++) {
                executor.execute(new ScanTask(ip, port));
            }
        }
    }

    private ScanReport buildReport() {
        List<HostReport> hostReports = new ArrayList<>();

        List<String> sortedHosts = new ArrayList<>(aliveHosts);
        sortedHosts.sort(Comparator.comparingLong(this::ipToLong));

        for (String host : sortedHosts) {
            Map<Integer, ScanResult> portMap = results.getOrDefault(host, new ConcurrentHashMap<>());

            List<ScanResult> sortedPorts = new ArrayList<>(portMap.values());
            sortedPorts.sort(Comparator.comparingInt(r -> r.port));

            hostReports.add(new HostReport(host, sortedPorts));
        }

        return new ScanReport(Instant.now().toString(), hostReports);
    }

    private class ScanTask implements Runnable {

        private final String ip;
        private final int port;

        ScanTask(String ip, int port) {
            this.ip = ip;
            this.port = port;
        }

        @Override
        public void run() {
            try {
                attempt();
            } catch (Exception e) {
                System.err.println("Worker error: " + e.getMessage());
            }
        }

        private void attempt() {
            int attempts = 0;
            while (attempts < 2) {
                attempts++;

                try (Socket socket = new Socket()) {
                    rateLimiter.acquire();
                    socket.connect(new InetSocketAddress(ip, port), config.connectTimeoutMs);
                    socket.setSoTimeout(config.readTimeoutMs);

                    aliveHosts.add(ip);

                    String banner = readBanner(socket);
                    String service = ServiceMapper.map(port);

                    results
                        .computeIfAbsent(ip, k -> new ConcurrentHashMap<>())
                        .put(port, new ScanResult(port, service, banner));

                    System.err.println("Open port: " + ip + ":" + port);
                    return;

                } catch (SocketTimeoutException e) {
                    if (attempts >= 2) return;
                } catch (ConnectException e) {
                    aliveHosts.add(ip);
                    return;
                } catch (Exception e) {
                    return;
                }
            }
        }

        private String readBanner(Socket socket) {
            try {
                byte[] buffer = new byte[256];
                int read = socket.getInputStream().read(buffer);
                if (read > 0) {
                    return new String(buffer, 0, read).trim();
                }
            } catch (Exception ignored) {}
            return null;
        }
    }

    private long ipToLong(String ip) {
        try {
            return ipToLong(InetAddress.getByName(ip));
        } catch (Exception e) {
            return 0;
        }
    }

    private long ipToLong(InetAddress ip) {
        byte[] octets = ip.getAddress();
        long result = 0;
        for (byte octet : octets) {
            result = (result << 8) | (octet & 0xff);
        }
        return result;
    }

    private String longToIp(long ip) {
        return String.format("%d.%d.%d.%d",
                (ip >> 24) & 0xff,
                (ip >> 16) & 0xff,
                (ip >> 8) & 0xff,
                ip & 0xff);
    }
}