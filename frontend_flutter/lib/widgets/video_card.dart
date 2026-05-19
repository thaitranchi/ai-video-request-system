import 'package:flutter/material.dart';
import '../models/video.dart';

class VideoCard extends StatelessWidget {
  final Video video; // Changed from VideoRequest to Video
  final VoidCallback? onWatch;

  const VideoCard({super.key, required this.video, this.onWatch});

  Color _getStatusColor() {
    switch (video.status) {
      case 'pending':
        return Colors.grey;
      case 'processing':
        return Colors.orange;
      case 'completed':
        return Colors.green;
      case 'failed':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              video.query,
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                  decoration: BoxDecoration(
                    color: _getStatusColor().withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: _getStatusColor()),
                  ),
                  child: Text(
                    video.status.toUpperCase(),
                    style: TextStyle(
                        color: _getStatusColor(),
                        fontSize: 12,
                        fontWeight: FontWeight.bold),
                  ),
                ),
                if (video.status == 'completed' && onWatch != null)
                  ElevatedButton.icon(
                    onPressed: onWatch,
                    icon: const Icon(Icons.play_arrow),
                    label: const Text('Watch'),
                  ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
