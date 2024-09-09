"use client";
import React, { useState, useEffect } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import ReactMarkdown from "react-markdown";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";

const CHAPTERS_PER_PAGE = 30;

const SummaryApp = () => {
  const [epubFiles, setEpubFiles] = useState([]);
  const [selectedEpub, setSelectedEpub] = useState("");
  const [chapters, setChapters] = useState([]);
  const [displayedChapters, setDisplayedChapters] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedChapters, setSelectedChapters] = useState([]);
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [summary, setSummary] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchEpubFiles();
  }, []);

  useEffect(() => {
    updateDisplayedChapters();
  }, [chapters, currentPage]);

  const updateDisplayedChapters = () => {
    const startIndex = (currentPage - 1) * CHAPTERS_PER_PAGE;
    const endIndex = startIndex + CHAPTERS_PER_PAGE;
    setDisplayedChapters(chapters.slice(startIndex, endIndex));
  };

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
      setCurrentPage(1);
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
      const response = await fetch(
        `book/summary/v1?book_id=${selectedEpub}&chapter_ids=${selectedChapters}`
      );
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

  const handleChapterToggle = (chapterId) => {
    setSelectedChapters((prev) =>
      prev.includes(chapterId)
        ? prev.filter((id) => id !== chapterId)
        : [...prev, chapterId]
    );
  };

  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
  };

  return (
    <div className="container mx-auto p-4">
      <div className="flex flex-col md:flex-row gap-4">
        <Card className="w-full max-w-3xl mx-auto">
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-center">
              RetainLLM - automate note-taking
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

                  {displayedChapters.length > 0 && (
                    <div>
                      <h3 className="font-semibold mb-2">Select chapters:</h3>
                      {displayedChapters.map((chapter) => (
                        <div
                          key={chapter.id}
                          className="flex items-center space-x-2"
                        >
                          <Checkbox
                            id={`chapter-${chapter.id}`}
                            checked={selectedChapters.includes(chapter.id)}
                            onCheckedChange={() =>
                              handleChapterToggle(chapter.id)
                            }
                          />
                          <label htmlFor={`chapter-${chapter.id}`}>
                            {chapter.title}
                          </label>
                        </div>
                      ))}
                      <div className="flex justify-between mt-4">
                        <Button
                          onClick={() => handlePageChange(currentPage - 1)}
                          disabled={currentPage === 1}
                        >
                          Previous
                        </Button>
                        <span>
                          Page {currentPage} of{" "}
                          {Math.ceil(chapters.length / CHAPTERS_PER_PAGE)}
                        </span>
                        <Button
                          onClick={() => handlePageChange(currentPage + 1)}
                          disabled={
                            currentPage ===
                            Math.ceil(chapters.length / CHAPTERS_PER_PAGE)
                          }
                        >
                          Next
                        </Button>
                      </div>
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
          </CardContent>
        </Card>
        <div className="w-full md:w-1/2">
          <Card className="h-full">
            <CardHeader>
              <CardTitle>Generated Summary</CardTitle>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <p className="text-center">Generating summary...</p>
              ) : summary ? (
                <ReactMarkdown>{summary}</ReactMarkdown>
              ) : (
                <p className="text-center text-gray-500">
                  No summary generated yet. Use the options on the left to
                  generate a summary.
                </p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default SummaryApp;
