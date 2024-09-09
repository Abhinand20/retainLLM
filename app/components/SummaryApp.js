"use client";
import React, { useState, useEffect } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const SummaryApp = () => {
  const [epubFiles, setEpubFiles] = useState([]);
  const [selectedEpub, setSelectedEpub] = useState("");
  const [chapters, setChapters] = useState([]);
  const [selectedChapters, setSelectedChapters] = useState([]);
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [summary, setSummary] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchEpubFiles();
  }, []);

  const fetchEpubFiles = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("/book/list");
      if (!response.ok) throw new Error("Failed to fetch list of books");
      const data = await response.json();
      console.log(data);
      setEpubFiles(data);
    } catch (error) {
      console.error("Error fetching books:", error);
    }
    setIsLoading(false);
  };

  const fetchChapters = async () => {
    if (!selectedEpub) return;
    setIsLoading(true);
    try {
      // Replace this with actual API call
      const response = await fetch(
        `/book/chapter/list?book_id=${selectedEpub}`
      );
      const data = await response.json();
      setChapters(data);
    } catch (error) {
      console.error("Error fetching chapters:", error);
    }
    setIsLoading(false);
  };

  const generateEpubSummary = async () => {
    if (selectedChapters.length === 0) return;
    setIsLoading(true);
    try {
      // Replace this with actual API call
      const response = await fetch("/api/epub-summary", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          file: selectedEpub,
          chapters: selectedChapters,
        }),
      });
      const data = await response.json();
      setSummary(data.summary);
    } catch (error) {
      console.error("Error generating ePub summary:", error);
    }
    setIsLoading(false);
  };

  const generateYoutubeSummary = async () => {
    if (!youtubeUrl) return;
    setIsLoading(true);
    try {
      // Replace this with actual API call
      const response = await fetch("/api/youtube-summary", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: youtubeUrl }),
      });
      const data = await response.json();
      setSummary(data.summary);
    } catch (error) {
      console.error("Error generating YouTube summary:", error);
    }
    setIsLoading(false);
  };

  return (
    <div className="container mx-auto p-4">
      <Card className="w-full max-w-3xl mx-auto">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">
            ePub and YouTube Summary Generator
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="epub" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="epub">ePub</TabsTrigger>
              <TabsTrigger value="youtube">YouTube</TabsTrigger>
            </TabsList>

            <TabsContent value="epub">
              <div className="space-y-4">
                <Select onValueChange={setSelectedEpub}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select an ePub file" />
                  </SelectTrigger>
                  <SelectContent>
                    {epubFiles.map((file) => (
                      <SelectItem key={file.id} value={file.id}>
                        {file.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>

                <Button
                  onClick={fetchChapters}
                  disabled={!selectedEpub || isLoading}
                >
                  List Chapters
                </Button>

                <Button
                  onClick={generateEpubSummary}
                  disabled={selectedChapters.length === 0 || isLoading}
                >
                  Generate ePub Summary
                </Button>

                {chapters.length > 0 && (
                  <div>
                    <h3 className="font-semibold mb-2">Select chapters:</h3>
                    {chapters.map((chapter) => (
                      <div
                        key={chapter.id}
                        className="flex items-center space-x-2"
                      >
                        <input
                          type="checkbox"
                          id={`chapter-${chapter.id}`}
                          checked={selectedChapters.includes(chapter.id)}
                          onChange={() => {
                            setSelectedChapters((prev) =>
                              prev.includes(chapter.id)
                                ? prev.filter((id) => id !== chapter.id)
                                : [...prev, chapter.id]
                            );
                          }}
                        />
                        <label htmlFor={`chapter-${chapter.id}`}>
                          {chapter.title}
                        </label>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </TabsContent>

            <TabsContent value="youtube">
              <div className="space-y-4">
                <Input
                  type="text"
                  placeholder="Enter YouTube URL"
                  value={youtubeUrl}
                  onChange={(e) => setYoutubeUrl(e.target.value)}
                />
                <Button
                  onClick={generateYoutubeSummary}
                  disabled={!youtubeUrl || isLoading}
                >
                  Generate YouTube Summary
                </Button>
              </div>
            </TabsContent>
          </Tabs>

          {isLoading && <p className="text-center mt-4">Processing...</p>}

          {summary && !isLoading && (
            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Generated Summary</CardTitle>
              </CardHeader>
              <CardContent>
                <p>{summary}</p>
              </CardContent>
            </Card>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default SummaryApp;
