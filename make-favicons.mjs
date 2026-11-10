// Regenerates KETE favicons from images/favicon.svg
import sharp from "sharp";
import pngToIco from "png-to-ico";
import { writeFileSync } from "fs";

const SRC = "images/favicon.svg";
const OUT = "images";

const sizes = {
  "favicon-32.png": 32,
  "favicon-48.png": 48,
  "favicon-96.png": 96,
  "favicon-192.png": 192,
  "apple-touch-icon.png": 180,
  "favicon-512.png": 512,
};

for (const [name, size] of Object.entries(sizes)) {
  await sharp(SRC, { density: 600 })
    .resize(size, size, { fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 } })
    .png()
    .toFile(`${OUT}/${name}`);
  console.log("wrote", name);
}

// Google still looks for /favicon.ico at the site root
const ico = await pngToIco([`${OUT}/favicon-48.png`, `${OUT}/favicon-32.png`]);
writeFileSync("favicon.ico", ico);
console.log("wrote favicon.ico");
