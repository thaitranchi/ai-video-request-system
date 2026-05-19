import 'package:flutter/material.dart';
import 'screens/request_screen.dart';
import 'screens/video_list_screen.dart';
import 'screens/video_player_screen.dart';
import 'models/video.dart';
import 'services/api_service.dart';
import 'core/constants.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Chemistry Video System',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
      ),
      home: const MainNavigation(),
    );
  }
}

class MainNavigation extends StatefulWidget {
  const MainNavigation({super.key});

  @override
  State<MainNavigation> createState() => _MainNavigationState();
}

class _MainNavigationState extends State<MainNavigation> {
  int _selectedIndex = 0;
  List<Video> _videos = [];

  @override
  void initState() {
    super.initState();
    _fetchVideos();
  }

  /// Fetches the latest video requests from the backend
  Future<void> _fetchVideos() async {
    try {
      final videos = await apiService.getVideos();
      setState(() {
        _videos = videos;
      });
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to load videos: $e')),
        );
      }
    } finally {
      // Finalize the request
    }
  }

  /// Navigates to the separate Video Player screen
  void _onVideoSelect(Video video) {
    String videoUrl = video.videoUrl ?? '';

    // If backend returns a relative path (e.g. starting with /videos),
    // prepend the correct host (10.0.2.2 for Android, localhost for others)
    if (videoUrl.startsWith('/')) {
      videoUrl = '${ApiConstants.serverRoot}$videoUrl';
    }

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => VideoPlayerScreen(
          videoUrl: videoUrl,
          title: video.query,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _selectedIndex,
        children: [
          const RequestScreen(),
          VideoListScreen(
            videos: _videos,
            onRefresh: _fetchVideos,
            onVideoSelect: _onVideoSelect,
          ),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) {
          setState(() => _selectedIndex = index);
          // Refresh list when switching to the Videos tab
          if (index == 1) _fetchVideos();
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.edit),
            label: 'Request',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.video_library),
            label: 'Videos',
          ),
        ],
      ),
    );
  }
}
