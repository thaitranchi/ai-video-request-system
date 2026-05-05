import 'dart:async';
import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/video.dart';
import '../widgets/video_card.dart';
import 'video_player_screen.dart';
import '../core/constants.dart';

class VideoListScreen extends StatefulWidget {
  const VideoListScreen({super.key});

  @override
  State<VideoListScreen> createState() => _VideoListScreenState();
}

class _VideoListScreenState extends State<VideoListScreen> {
  List<VideoRequest> _videos = [];
  bool _isLoading = true;
  Timer? _pollingTimer;

  @override
  void initState() {
    super.initState();
    _fetchVideos();
    // Auto-refresh every 5 seconds to track progress
    _pollingTimer = Timer.periodic(const Duration(seconds: 5), (_) => _fetchVideos(quiet: true));
  }

  @override
  void dispose() {
    _pollingTimer?.cancel();
    super.dispose();
  }

  Future<void> _fetchVideos({bool quiet = false}) async {
    if (!quiet) setState(() => _isLoading = true);
    try {
      final videos = await apiService.getVideos();
      setState(() {
        _videos = videos.reversed.toList(); // Newest first
        _isLoading = false;
      });
    } catch (e) {
      if (!quiet) {
        setState(() => _isLoading = false);
        debugPrint('Error fetching: $e');
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("My Video Requests"),
        actions: [
          IconButton(onPressed: _fetchVideos, icon: const Icon(Icons.refresh))
        ],
      ),
      body: _isLoading 
          ? const Center(child: CircularProgressIndicator())
          : _videos.isEmpty
              ? const Center(child: Text("No requests yet. Try creating one!"))
              : RefreshIndicator(
                  onRefresh: _fetchVideos,
                  child: ListView.builder(
                    itemCount: _videos.length,
                    itemBuilder: (context, index) {
                      final video = _videos[index];
                      return VideoCard(
                        video: video,
                        onWatch: video.status == VideoStatus.completed && video.videoUrl != null
                            ? () {
                                final fullUrl = '${ApiConstants.serverRoot}${video.videoUrl}';
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) => VideoPlayerScreen(
                                      videoUrl: fullUrl,
                                      title: video.query,
                                    ),
                                  ),
                                );
                              }
                            : null,
                      );
                    },
                  ),
                ),
    );
  }
}