import { Search } from 'lucide-react';
import React, { useEffect, useState } from 'react';
import Papa from 'papaparse';

const Card = ({ children }) => <div className="border rounded-lg shadow-lg p-4">{children}</div>;
const CardHeader = ({ children }) => <div className="mb-4">{children}</div>;
const CardContent = ({ children }) => <div>{children}</div>;

const ProductVideo = ({ username, views, length, summary, thumbnail, link, title, tags }) => (
  <div className="mt-4 flex flex-col md:flex-row">
    <div className="w-full md:w-1/3 md:mr-4 mb-4 md:mb-0">
      <a href={link} target="_blank" rel="noopener noreferrer">
        <img src={thumbnail} alt="Video thumbnail" className="w-full rounded-lg flex-row" />
      </a>
    </div>
    <div className="w-full md:w-2/3">
      <p className="text-lg font-bold">{title}</p>
      <p className="text-sm">
        <span className="font-semibold">{username}</span> {views} • {length}
      </p>
      <p className="text-gray-600 text-sm mt-1">{summary}</p>
      <div className="mt-2 flex flex-wrap">
        {tags.map((tag, index) => (
          <Tag key={index} tag={tag} />
        ))}
      </div>
    </div>
  </div>
);  

const Tag = ({ tag }) => {
  const colors = ["blue", "green", "yellow"];
  const colorIndex = tag.charCodeAt(0) % 3;
  const bgColor = colors[colorIndex];
  
  return (
    <button className={`bg-${bgColor}-500 hover:bg-${bgColor}-600 text-white font-semibold py-1 px-2 rounded text-sm mr-2 mb-2`}>
      {tag}
    </button>
  );
};

const BeautyProductWebsite = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [videos, setVideos] = useState([]);
  const [productSummaries, setProductSummaries] = useState({});

  useEffect(() => {
    const fetchVideos = async () => {
      try {
        const response = await fetch('/video.csv');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const csvData = await response.text();
        const parsedData = Papa.parse(csvData, { header: true }).data;
        console.log('Parsed Data:', parsedData);
        
        const videoEntries = parsedData.filter(entry => !entry.username.startsWith('summary_'));
        setVideos(videoEntries);
        
        const summaries = {};
        parsedData.forEach(entry => {
          if (entry.username.startsWith('summary_')) {
            const productName = entry.username.replace('summary_', '');
            summaries[productName.toLowerCase()] = entry.summary;
          }
        });
        setProductSummaries(summaries);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchVideos();
  }, []);

  const filteredVideos = videos.filter((video) =>
    video.product && video.product.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const renderProductVideos = () => {
    if (searchQuery.trim() === '') {
      return null;
    }
    
    return filteredVideos.map((video, index) => {
      const tags = [];
      for (let i = 1; i <= 10; i++) {
        if (video[`tag${i}`]) {
          tags.push(video[`tag${i}`]);
        }
      }
      
      return (
        <ProductVideo
          key={index}
          username={video.username}
          views={video.views}
          length={video.length}
          summary={video.summary}
          thumbnail={video.thumbnail}
          link={video.link}
          title={video.name}
          tags={tags}
        />
      );
    });
  };

  const renderTrendReport = () => {
    if (searchQuery.trim() === '') {
      return (
        <>
          <h2 className="text-2xl font-bold mb-4">Trend Report</h2>
          <p className="text-gray-600 mb-8">
            Our AI-generated summaries provide a snapshot of what people are saying about the latest beauty products. With each search, you'll get a quick overview of all the product videos approved by industry veterans.
          </p>
        </>
      );
    }

    const matchedProduct = Object.keys(productSummaries).find(product => 
      product.includes(searchQuery.toLowerCase())
    );

    if (matchedProduct && productSummaries[matchedProduct]) {
      return (
        <>
          <h2 className="text-2xl font-bold mb-4">AI-Generated Summary for {matchedProduct.charAt(0).toUpperCase() + matchedProduct.slice(1)}</h2>
          <p className="text-gray-600 mb-8">{productSummaries[matchedProduct]}</p>
        </>
      );
    } else {
      return (
        <>
          <h2 className="text-2xl font-bold mb-4">Trend Report</h2>
          <p className="text-gray-600 mb-8">
            Our AI-generated summaries provide a snapshot of what people are saying about the latest beauty products. With each search, you'll get a quick overview of all the product videos approved by industry veterans.
          </p>
        </>
      );
    }
  };  

  return (
    <div className="bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row justify-between items-center border-b-2 border-gray-100 py-6 md:justify-start md:space-x-10">
          <div className="flex justify-start lg:w-0 lg:flex-1 mb-4 sm:mb-0">
            <span className="text-2xl font-bold text-gray-900">Landing International</span>
          </div>
          <div className="flex items-center justify-end md:flex-1 lg:w-0">
            <a
              href="/"
              className="ml-4 whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-blue-600 hover:bg-blue-700"
            >
              Home
            </a>
            <a
              href="#"
              className="ml-4 whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-blue-600 hover:bg-blue-700"
            >
              Log In
            </a>
            <a
              href="#"
              className="ml-4 whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-blue-600 hover:bg-blue-700"
            >
              Sign Up
            </a>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          Industry-vetted videos
          <br />
          Product expertise in seconds
        </h1>
        <h2 className="text-xl font-medium text-gray-900 mb-4">
          Finding helpful product review videos takes time. We do it for you in seconds. Get up to speed on the latest beauty products from industry-vetted videos that actually help you decide what's right for you.
        </h2>

        <div className="mt-12 w-full">
          <Card>
            <CardContent>
              <div className="relative mb-6">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Search className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="text"
                  placeholder="Search products"
                  className="block w-full pl-10 pr-3 py-3 sm:text-sm border-gray-300 rounded-md leading-5 bg-white focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
              <CardHeader>
                {renderTrendReport()}
              </CardHeader>
              {renderProductVideos()}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Home;