#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            BYTE newcolor = 0; // counting average
            newcolor =
                round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = newcolor;
            image[i][j].rgbtGreen = newcolor;
            image[i][j].rgbtRed = newcolor;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++) // just going to half of width!
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp; // also decreasing 1 because of 0-indexing
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE blurredImage[height]
                          [width]; // working on a copy to avoid modyfing pixels during loops
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++) // for each pixel from the image
        {
            WORD newRed = 0;
            WORD newGreen = 0;
            WORD newBlue = 0; // using WORD (uint16_t) to avoid overflow
            double existingPixels = 0.0;
            for (int x = -1; x <= 1; x++)
            {
                for (int y = -1; y <= 1; y++) // each pixel in range 1
                {
                    if ((0 <= i + x && i + x < height) && (0 <= j + y && j + y < width))
                    { // 0<= and <height because of 0-indexing again, image[i][height] doesn't exist
                        newRed += image[i + x][j + y].rgbtRed;
                        newGreen += image[i + x][j + y].rgbtGreen;
                        newBlue += image[i + x][j + y].rgbtBlue;
                        existingPixels++;
                    }
                }
            }
            blurredImage[i][j].rgbtRed = round(newRed / existingPixels);
            blurredImage[i][j].rgbtGreen = round(newGreen / existingPixels);
            blurredImage[i][j].rgbtBlue = round(newBlue / existingPixels);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = blurredImage[i][j]; // copying each element to original image
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{ // we will use similar logic to blur filter - creating a new image to help us
    RGBTRIPLE edgeImage[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++) // for each pixel from the image
        {
            int gx_kernel[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
            int gy_kernel[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
            int countOne = 0;
            int countTwo = 0; // count to access correct values in kernels
            long gxRGB[] = {0, 0, 0};
            long gyRGB[] = {0, 0, 0}; // using longs to acces negative values
            WORD RGB[] = {0, 0, 0};   // final RGB values for that pixel
            for (int x = -1; x <= 1; x++)
            {
                for (int y = -1; y <= 1; y++) // each pixel in range 1
                {
                    if ((0 <= i + x && i + x < height) && (0 <= j + y && j + y < width))
                    { // 0<= and <height because of 0-indexing again, image[i][height] doesn't exist
                        gxRGB[0] += image[i + x][j + y].rgbtRed * gx_kernel[countOne][countTwo];
                        gxRGB[1] += image[i + x][j + y].rgbtGreen * gx_kernel[countOne][countTwo];
                        gxRGB[2] += image[i + x][j + y].rgbtBlue * gx_kernel[countOne][countTwo];

                        gyRGB[0] += image[i + x][j + y].rgbtRed * gy_kernel[countOne][countTwo];
                        gyRGB[1] += image[i + x][j + y].rgbtGreen * gy_kernel[countOne][countTwo];
                        gyRGB[2] += image[i + x][j + y].rgbtBlue * gy_kernel[countOne][countTwo];
                    }
                    countTwo++;
                }
                countTwo = 0;
                countOne++;
            }
            countTwo = 0;

            for (int k = 0; k < 3; k++)
            {
                RGB[k] = round(sqrt(pow(gxRGB[k], 2.0) + pow(gyRGB[k], 2.0)));
                if (RGB[k] > 255)
                {
                    RGB[k] = 255;
                }
            }
            edgeImage[i][j].rgbtBlue = RGB[2];
            edgeImage[i][j].rgbtGreen = RGB[1];
            edgeImage[i][j].rgbtRed = RGB[0];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = edgeImage[i][j];
        }
    }
}
